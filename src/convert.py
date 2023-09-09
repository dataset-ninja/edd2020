import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size

# import shutil
import cv2

from tqdm import tqdm


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer...", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = "/mnt/c/users/german/documents/EndoCV2020-Endoscopy-Disease-Detection-Segmentation-subChallenge_data/bbox"
    masks_path = "/mnt/c/Users/German/Documents/EndoCV2020-Endoscopy-Disease-Detection-Segmentation-subChallenge_data/masks"

    # create project and initialize meta
    project = api.project.create(workspace_id, project_name)
    meta = sly.ProjectMeta()

    # read class names and create classes for them
    directory = os.path.dirname(dataset_path)
    with open(directory + "/class_list.txt") as class_file:
        class_names = class_file.read().split("\n")

    for name in class_names:
        if name == "":
            break
        obj_class = sly.ObjClass(name + "_bbox", sly.Rectangle)
        meta = meta.add_obj_class(obj_class)
        obj_class_mask = sly.ObjClass(name, sly.Bitmap)
        meta = meta.add_obj_class(obj_class_mask)
    api.project.update_meta(project.id, meta)

    # create dataset
    dataset = api.dataset.create(project.id, "ds0")

    # get a list of images and iterate over it
    image_paths = sly.fs.list_files(
        os.path.join(os.path.dirname(dataset_path), "originalImages"),
        valid_extensions=[".jpg"],
    )
    pbar = tqdm(total=len(image_paths), desc="images")
    for path in image_paths:
        image_filename = sly.fs.get_file_name(path)
        bbox_ann_path = os.path.join(dataset_path, (image_filename + ".txt"))
        try:
            # upload an image
            image_info = api.image.upload_path(dataset.id, image_filename, path)

            # read bbox annotation
            output = []
            with open(bbox_ann_path) as file:
                file_split = file.read().rstrip().split("\n")
            for row in file_split:
                if row == "":
                    continue
                output.append(row.split())

            # upload annotations
            labels = []
            for bbox in output:
                xmin, ymin, xmax, ymax, c = bbox

                bbox_annotation = sly.Rectangle(int(ymin), int(xmin), int(ymax), int(xmax))
                obj_class = meta.get_obj_class(c + "_bbox")
                label = sly.Label(bbox_annotation, obj_class)
                labels.append(label)

            for file in sly.fs.list_files(masks_path, valid_extensions=[".tif"]):
                if image_filename in file:
                    class_name = sly.fs.get_file_name(file).rstrip().split("_")[2]
                    mask = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
                    mask_ann = sly.Bitmap(mask)
                    obj_class_mask = meta.get_obj_class(class_name)
                    label = sly.Label(mask_ann, obj_class_mask)
                    labels.append(label)

            ann = sly.Annotation(img_size=[image_info.height, image_info.width], labels=labels)
            api.annotation.upload_ann(image_info.id, ann)
            pbar.update(1)
        except Exception as e:
            print(e)
            pbar.update(1)
            continue
    pbar.close()
    print(f"Dataset (id:{dataset.id}) has been successfully created.")

    return project
