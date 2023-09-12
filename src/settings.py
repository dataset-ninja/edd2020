from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "EDD2020"
PROJECT_NAME_FULL: str = "EDD2020: Endoscopy Disease Detection and Segmentation"
HIDE_DATASET = True  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_NC_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Medical()]
CATEGORY: Category = Category.Medical(sensitive_content=True)

CV_TASKS: List[CVTask] = [
    CVTask.ObjectDetection(),
    CVTask.InstanceSegmentation(),
    CVTask.SemanticSegmentation(),
]
ANNOTATION_TYPES: List[AnnotationType] = [
    AnnotationType.ObjectDetection(),
    AnnotationType.InstanceSegmentation(),
]

RELEASE_DATE: Optional[str] = "2020-06-03"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = (
    "https://ieee-dataport.org/competitions/endoscopy-disease-detection-and-segmentation-edd2020"
)
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 3547192
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/edd2020"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[
    Union[str, dict]
] = "https://ieee-dataport.s3.amazonaws.com/competition/6486/EndoCV2020-Endoscopy-Disease-Detection-Segmentation-subChallenge_data.zip?response-content-disposition=attachment%3B%20filename%3D%22EndoCV2020-Endoscopy-Disease-Detection-Segmentation-subChallenge_data.zip%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJOHYI4KJCE6Q7MIQ%2F20230911%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230911T193359Z&X-Amz-SignedHeaders=Host&X-Amz-Expires=86400&X-Amz-Signature=584a80f54dd7c2aebb2f8a6fa989c9fb1ce3f810e303b60878d306695275de40"
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = "https://arxiv.org/abs/2003.03376"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[
    Union[str, List[str], Dict[str, str]]
] = "https://github.com/sharib-vision/EDD2020"

CITATION_URL: Optional[str] = ""
AUTHORS: Optional[List[str]] = [
    "Sharib Ali",
    "Barbara Braden",
    "Dominique Lamarque",
    "Stefano Realdon",
    "Adam Bailey",
    "Renato Cannizzaro",
    "Noha Ghatwary",
    "Jens Rittscher",
    "Christian Daul",
    "James East",
]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = ["UK, Italy, France joint research team"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = None

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = None
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
