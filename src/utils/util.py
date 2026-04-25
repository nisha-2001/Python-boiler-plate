# pylint: disable=missing-module-docstring,broad-exception-caught,import-error,missing-class-docstring, missing-function-docstring, too-few-public-methods logging-fstring-interpolation,global-variable-not-assigned
import json
import logging
import os
import re
import threading

from google.cloud import storage

from src.commons.exceptions.custom_processor_error import CustomProcessorError

logger = logging.getLogger(__name__)

# Global cache for storing loaded files
loaded_files_cache = {}
cache_lock = threading.Lock()

__BASE_DIR = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-2]) + "/"


def read_json(file_path):
    """
    :param file_path: json file path
    :return: python dictionary
    """
    data = {}
    try:
        with open(file_path, "r", encoding="UTF-8") as j_file:
            data = json.load(j_file)
            logger.debug(f"Loading file from {file_path}")
    except FileNotFoundError:
        logging.error("No File found for processing : %s", file_path)
    return data


def load_files_from_cloud_storage(bucket, file_path, is_local):
    global loaded_files_cache

    # If saved in first load - return the file [Lazy Loading]
    with cache_lock:
        if file_path in loaded_files_cache:
            return loaded_files_cache[file_path]
    logger.info(f"Initializing File Loading, Local = {is_local}")
    if is_local:
        resource_path = __BASE_DIR + file_path
        logger.info(f"Loading Local Data - {resource_path}")
        file_content = read_json(resource_path)
    else:
        try:
            logger.info("Initializing file storage")
            client = storage.Client()
            bucket = client.get_bucket(bucket)
            blob = bucket.get_blob(file_path)
            logger.info("File Blob %s", blob)
            logger.info("Starting download of file from GCS: %s", file_path)
            file_content = json.loads(blob.download_as_string())
            logger.info("Successfully downloaded file from GCS: %s", file_path)
        except CustomProcessorError as e:
            logger.error(
                "File Downloading failed  %s with file name %s", str(e), file_path
            )
            return None

    with cache_lock:
        loaded_files_cache[file_path] = file_content

    return file_content


def normalize_generic_context(context):
    context = re.sub(r"&amp;", " ", context)
    context = re.sub(r"\s+", " ", context)
    return context


def get_collection(tenant, site, site_override):
    if site_override:
        return tenant
    return f"{tenant}_{site}" if site and site != tenant else tenant
