# https://limu.ait.kyushu-u.ac.jp/~agri/komatsuna/

import os
import shutil
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


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


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "KOMATSUNA dataset"
    images_path = "/mnt/d/datasetninja-raw/komatsuna/multi_plant/multi_plant"
    orig_images_path = "/mnt/d/datasetninja-raw/komatsuna/multi_original/multi_original"
    masks_path = "/mnt/d/datasetninja-raw/komatsuna/multi_label/multi_label"
    batch_size = 30
    masks_prefix = "label"
    ds_name = "multi-view"

    def get_unique_colors(img):
        unique_colors = []
        img = img.astype(np.int32)
        h, w = img.shape[:2]
        colhash = img[:, :, 0] * 256 * 256 + img[:, :, 1] * 256 + img[:, :, 2]
        unq, unq_inv, unq_cnt = np.unique(colhash, return_inverse=True, return_counts=True)
        indxs = np.split(np.argsort(unq_inv), np.cumsum(unq_cnt[:-1]))
        col2indx = {unq[i]: indxs[i][0] for i in range(len(unq))}
        for col, indx in col2indx.items():
            if col != 0:
                unique_colors.append((col // (256**2), (col // 256) % 256, col % 256))

        return unique_colors

    color_to_oldest = {
        (0, 0, 255): 1,
        (0, 255, 0): 2,
        (0, 255, 255): 3,
        (255, 0, 0): 4,
        (255, 0, 255): 5,
        (255, 255, 0): 6,
        (128, 128, 128): 7,
        (0, 0, 128): 8,
    }

    def create_ann(image_path):
        labels = []

        mask_name = masks_prefix + get_file_name_with_ext(image_path)[3:]
        mask_path = os.path.join(masks_path, mask_name)

        img_np = sly.imaging.image.read(image_path)
        img_height = img_np.shape[0]
        img_wight = img_np.shape[1]

        if not "rgbd" in image_path:
            if "_original/" in image_path:
                # see official docs for explanation
                _, AA, CCC, DD = get_file_name(image_path).split("_")
            elif "_plant/" in image_path:
                _, AA, BB, CCC, DD = get_file_name(image_path).split("_")

            im_id = f"{AA}_{CCC}_{DD}"
        else:
            if "_original/" in image_path:
                # see official docs for explanation
                _, CCC, DD = get_file_name(image_path).split("_")
            elif "_plant/" in image_path:
                _, BB, CCC, DD = get_file_name(image_path).split("_")
            im_id = f"{CCC}_{DD}"

        group_tag = sly.Tag(group_tag_meta, value=im_id)

        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)

            unique_colors = get_unique_colors(mask_np)
            for color in unique_colors:
                mask = np.all(mask_np == color, axis=2)
                ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    curr_bitmap = sly.Bitmap(obj_mask)
                    if color_to_oldest.get(color) is not None:
                        tg = [sly.Tag(leaf_tag_meta, color_to_oldest[color])]
                    else:
                        tg = []
                    curr_label = sly.Label(curr_bitmap, obj_class, tg)
                    labels.append(curr_label)

        tag_name = image_path.split("/")[-2]  # for example
        tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == tag_name]
        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=[group_tag] + tags
        )

    obj_class = sly.ObjClass("leaf", sly.Bitmap)

    tag_names = [
        "multi_original",
        "multi_plant",
        "rgbd_original",
        "rgbd_plant",
        "rgbd_depth",
        "rgbd_depth_ours",
    ]
    tag_metas = [sly.TagMeta(name, sly.TagValueType.NONE) for name in tag_names]

    group_tag_meta = sly.TagMeta("im_id", sly.TagValueType.ANY_STRING)
    leaf_tag_meta = sly.TagMeta("old", sly.TagValueType.ANY_NUMBER)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class], tag_metas=[group_tag_meta, leaf_tag_meta] + tag_metas
    )

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_meta.name)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)
    images_names = os.listdir(images_path)

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for img_names_batch in sly.batched(images_names, batch_size=batch_size):
        img_pathes_batch = [os.path.join(images_path, im_name) for im_name in img_names_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    # =========== add orig images multi ds ==========================================================================
    orig_images_names = os.listdir(orig_images_path)
    progress = sly.Progress("Create dataset {}".format(ds_name), len(orig_images_names))
    for img_names_batch in sly.batched(orig_images_names, batch_size=batch_size):
        img_pathes_batch = [os.path.join(orig_images_path, im_name) for im_name in img_names_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    # =========== add rgb-d ds ======================================================================================

    def create_ann_orig(image_path):
        # tag_names = []

        img_np = sly.imaging.image.read(image_path)
        img_height = img_np.shape[0]
        img_wight = img_np.shape[1]

        if "rgbd_original" or "_depth" in image_path:
            # see official docs for explanation
            _, CCC, DD = get_file_name(image_path).split("_")
        elif "rgbd_plant" in image_path:
            _, BB, CCC, DD = get_file_name(image_path).split("_")

        im_id = f"{CCC}_{DD}"
        group_tag = sly.Tag(group_tag_meta, value=im_id)

        tag_name = image_path.split("/")[-2]
        tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == tag_name]
        return sly.Annotation(img_size=(img_height, img_wight), img_tags=[group_tag] + tags)

    images_path = "/mnt/d/datasetninja-raw/komatsuna/rgbd_plant/rgbd_plant"
    orig_images_path = "/mnt/d/datasetninja-raw/komatsuna/rgbd_original/rgbd_original"
    masks_path = "/mnt/d/datasetninja-raw/komatsuna/rgbd_label/rgbd_label"
    rgbd_depth_path = "/mnt/d/datasetninja-raw/komatsuna/rgbd_depth/rgbd_depth"
    rgbd_depth_ours_path = "/mnt/d/datasetninja-raw/komatsuna/rgbd_depth_ours/rgbd_depth_ours"
    batch_size = 30
    masks_prefix = "label"
    rgb_prefix = "rgb"
    depth_prefix = "depth"
    ds_name = "rgb-d"
    # group_tag_name = "im_id"

    # group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)
    # meta = meta.add_tag_meta(group_tag_meta)
    api.project.update_meta(project.id, meta.to_json())
    # api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_names = os.listdir(images_path)

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for img_names_batch in sly.batched(images_names, batch_size=batch_size):
        img_pathes_batch = [os.path.join(images_path, im_name) for im_name in img_names_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    # =========== add orig images rgb-d ds ==========================================================================
    orig_images_names = os.listdir(orig_images_path)
    progress = sly.Progress("Create dataset {}".format(ds_name), len(orig_images_names))
    for img_names_batch in sly.batched(orig_images_names, batch_size=batch_size):
        img_pathes_batch = []
        images_names_batch = []
        for im_name in img_names_batch:
            depth_name = im_name.replace(rgb_prefix, depth_prefix)
            depth_ours_name = "ours_" + depth_name
            images_names_batch.extend([im_name, depth_name, depth_ours_name])

            im_path = os.path.join(orig_images_path, im_name)
            depth_path = os.path.join(rgbd_depth_path, depth_name)
            depth_ours_path = os.path.join(rgbd_depth_ours_path, depth_name)

            img_pathes_batch.extend([im_path, depth_path, depth_ours_path])

        img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = []
        for i in range(0, len(img_pathes_batch), 3):
            ann0 = create_ann_orig(img_pathes_batch[i])
            ann1 = create_ann_orig(img_pathes_batch[i + 1])
            ann2 = create_ann_orig(img_pathes_batch[i + 2])
            anns.extend([ann0, ann1, ann2])
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))
    return project
