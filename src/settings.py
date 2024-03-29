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
PROJECT_NAME: str = "KOMATSUNA"
PROJECT_NAME_FULL: str = "KOMATSUNA Dataset for Instance Segmentation, Tracking and Reconstruction"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.PubliclyAvailable(
    source_url="https://openaccess.thecvf.com/content_ICCV_2017_workshops/papers/w29/Uchiyama_An_Easy-To-Setup_3D_ICCV_2017_paper.pdf"
)
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Research.Biological()]
CATEGORY: Category = Category.Biology()

CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.SemanticSegmentation(),
    CVTask.ObjectDetection(),
    CVTask.MonocularDepthEstimation(),
]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2017

HOMEPAGE_URL: str = "https://limu.ait.kyushu-u.ac.jp/~agri/komatsuna/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 12690903
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/komatsuna"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = (
    "https://limu.ait.kyushu-u.ac.jp/~agri/komatsuna/"
)
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = {
    "Research Paper": "https://openaccess.thecvf.com/content_ICCV_2017_workshops/papers/w29/Uchiyama_An_Easy-To-Setup_3D_ICCV_2017_paper.pdf",
    "RGBD Readme": "https://limu.ait.kyushu-u.ac.jp/~agri/komatsuna/rgbd_readme.pdf",
    "Multi-View Readme": "https://limu.ait.kyushu-u.ac.jp/~agri/komatsuna/multi_readme.pdf",
}
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = None

CITATION_URL: Optional[str] = "https://openaccess.thecvf.com/ICCV2017_workshops/ICCV2017_W29"
AUTHORS: Optional[List[str]] = [
    "Hideaki Uchiyama",
    "Shunsuke Sakurai",
    "Masashi Mishima",
    "Daisaku Arita",
    "Takashi Okayasu",
    "Atsushi Shimada",
    "Rin-ichiro Taniguchi",
]
AUTHORS_CONTACTS: Optional[List[str]] = ["agri@limu.ait.kyushu-u.ac.jp"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = ["Kyushu University, Japan"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = ["https://www.kyushu-u.ac.jp/en/"]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "image splits": [
        "multi_original",
        "multi_plant",
        "rgbd_original",
        "rgbd_plant",
        "rgbd_depth",
        "rgbd_depth_ours",
    ],
    "__POSTTEXT__": "Additionally, images are grouped by ***im_id***, and every *leaf* has ***old*** tag. Explore it in supervisely labeling tool",
}
TAGS: Optional[List[str]] = ['multi-view']


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
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
