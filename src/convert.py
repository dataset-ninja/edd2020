import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil
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
    datasets = [
        "/mnt/c/users/german/documents/EndoCV2020-Endoscopy-Disease-Detection-Segmentation-subChallenge_data/masks",
        "/mnt/c/users/german/documents/EndoCV2020-Endoscopy-Disease-Detection-Segmentation-subChallenge_data/bbox",
    ]

    directory = os.path.dirname(datasets[0])
    with open(directory + "/class_list.txt") as class_file:
        class_names = class_file.read().split("\n")

    project = api.project.create(workspace_id, project_name)
    meta = sly.ProjectMeta()

    for name in class_names:
        if name == "":
            break
        obj_class = sly.ObjClass(name + "_bbox", sly.Rectangle)
        meta = meta.add_obj_class(obj_class)
        obj_class_mask = sly.ObjClass(name, sly.Bitmap)
        meta = meta.add_obj_class(obj_class_mask)

    api.project.update_meta(project.id, meta)

    def load_image_labels(image_path, labels_path):
        image_info = api.image.upload_path(
            dataset_bboxes.id, os.path.basename(image_path), image_path
        )
        output = []
        with open(labels_path) as file:
            file_split = file.read().rstrip().split("\n")
        for row in file_split:
            if row == "":
                continue
            output.append(row.split())
        labels = []
        height = image_info.height
        width = image_info.width
        for bbox in output:
            xmin, ymin, xmax, ymax, c = bbox

            bbox_annotation = sly.Rectangle(int(ymin), int(xmin), int(ymax), int(xmax))
            obj_class = meta.get_obj_class(c + "_bbox")
            label = sly.Label(bbox_annotation, obj_class)
            labels.append(label)
        ann = sly.Annotation(img_size=[height, width], labels=labels)
        api.annotation.upload_ann(image_info.id, ann)

    def load_image_labels_mask(image_path, labels_path, class_name):
        image_info = api.image.get_info_by_name(dataset_mask.id, os.path.basename(image_path))
        if image_info is None:
            image_info = api.image.upload_path(
                dataset_mask.id, os.path.basename(image_path), image_path
            )
        mask = cv2.imread(labels_path, cv2.IMREAD_GRAYSCALE)
        labels = []
        height = image_info.height
        width = image_info.width
        bitmap_annotation = sly.Bitmap(mask)
        obj_class = meta.get_obj_class(class_name)
        label = sly.Label(bitmap_annotation, obj_class)
        labels.append(label)

        ann: sly.Annotation = sly.Annotation.from_json(
            api.annotation.download_json(image_info.id), meta
        )
        ann = ann.add_labels(labels)
        # ann = sly.Annotation(img_size=[height, width], labels=labels)
        api.annotation.upload_ann(image_info.id, ann)

    mask_paths = sly.fs.list_files(datasets[0], valid_extensions=[".tif"])
    bbox_paths = sly.fs.list_files(datasets[1], valid_extensions=[".txt"])

    dataset_mask = api.dataset.create(project.id, os.path.basename(datasets[0]))
    dataset_bboxes = api.dataset.create(project.id, os.path.basename(datasets[1]))

    image_paths = sly.fs.list_files(
        os.path.join(os.path.dirname(datasets[0]), "originalImages"),
        valid_extensions=[".jpg"],
    )
    pbar = tqdm(total=len(image_paths), desc="images")
    for path in image_paths:
        image_filename = sly.fs.get_file_name(path)
        try:
            load_image_labels(
                path, os.path.join(datasets[1], (os.path.basename(path)[:-4] + ".txt"))
            )
            pbar.update(1)
        except Exception as e:
            print(e)
            pbar.update(1)
            continue
        for mask in mask_paths:
            mask_filename = sly.fs.get_file_name(mask)
            mask_filename_parts = mask_filename.rstrip().split("_")
            single_mask_name = mask_filename_parts[0] + "_" + mask_filename_parts[1]
            class_name = mask_filename_parts[2]
            if single_mask_name == image_filename:
                try:
                    load_image_labels_mask(path, mask, class_name)
                    pbar.update(1)
                except Exception as e:
                    print(e)
                    pbar.update(1)
                    continue
    pbar.close()

    print(f"Dataset (id:{dataset_mask.id}) has been successfully created.")

    return project
