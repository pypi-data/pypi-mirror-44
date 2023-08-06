""" Utilities - Helper functions """

import collections
import os
import pickle
import re
import time

import math
import pkg_resources
import rapidjson
import requests
import shapely.geometry
import tqdm


# Type to confirm whether to proceed or not
def confirmed(prompt=None, resp=False, confirmation_required=True):
    """
    Reference: http://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/

    :param prompt: [str] or None
    :param resp: [bool]
    :param confirmation_required: [bool]
    :return:

    Example: confirm(prompt="Create Directory?", resp=True)
             Create Directory? Yes|No:

    """
    if confirmation_required:
        if prompt is None:
            prompt = "Confirmed? "

        if resp is True:  # meaning that default response is True
            prompt = "{} [{}]|{}: ".format(prompt, "Yes", "No")
        else:
            prompt = "{} [{}]|{}: ".format(prompt, "No", "Yes")

        ans = input(prompt)
        if not ans:
            return resp

        if re.match('[Yy](es)?', ans):
            return True
        if re.match('[Nn](o)?', ans):
            return False

    else:
        return True


# ====================================================================================================================
""" Change directory """


# Change directory and sub-directories
def cd(*directories):
    # Current working directory
    path = os.getcwd()
    for directory in directories:
        path = os.path.join(path, directory)
    return path


# Change directory to "dat_GeoFabrik" and sub-directories
def cd_dat_geofabrik(*directories):
    path = cd("dat_GeoFabrik")
    for directory in directories:
        path = os.path.join(path, directory)
    return path


# Change directory to "dat_BBBike" and sub-directories
def cd_dat_bbbike(*directories):
    path = cd("dat_BBBike")
    for directory in directories:
        path = os.path.join(path, directory)
    return path


# Change directory to "dat" and sub-directories
def cd_dat(*directories):
    path = pkg_resources.resource_filename(__name__, 'dat/')
    for directory in directories:
        path = os.path.join(path, directory)
    return path


# Regulate the input data directory
def regulate_input_data_dir(data_dir):
    """
    :param data_dir: [str] data directory as input
    :return: [str] regulated data directory
    """
    assert isinstance(data_dir, str)
    regulated_dir = os.path.realpath(data_dir.lstrip('.\\'))
    assert os.path.isabs(regulated_dir), "'download_dir' is invalid."
    return regulated_dir


# ====================================================================================================================
""" Save and Load files """


# Save pickles
def save_pickle(pickle_data, path_to_pickle):
    """
    :param pickle_data: any object that could be dumped by the 'pickle' package
    :param path_to_pickle: [str] local file path
    :return: whether the data has been successfully saved
    """
    pickle_filename = os.path.basename(path_to_pickle)
    print("{} \"{}\" ... ".format("Updating" if os.path.isfile(path_to_pickle) else "Saving", pickle_filename), end="")
    try:
        os.makedirs(os.path.dirname(path_to_pickle), exist_ok=True)
        pickle_out = open(path_to_pickle, 'wb')
        pickle.dump(pickle_data, pickle_out)
        pickle_out.close()
        print("Done.")
    except Exception as e:
        print("Failed. {}.".format(e))


# Load pickles
def load_pickle(path_to_pickle):
    """
    :param path_to_pickle: [str] local file path
    :return: the object retrieved from the pickle
    """
    pickle_in = open(path_to_pickle, 'rb')
    data = pickle.load(pickle_in)
    pickle_in.close()
    return data


# Save JSON files
def save_json(json_data, path_to_json):
    """
    :param json_data: any object that could be dumped by the 'json' package
    :param path_to_json: [str] local file path
    :return: whether the data has been successfully saved
    """
    json_filename = os.path.basename(path_to_json)
    print("{} \"{}\" ... ".format("Updating" if os.path.isfile(path_to_json) else "Saving", json_filename), end="")
    try:
        os.makedirs(os.path.dirname(path_to_json), exist_ok=True)
        json_out = open(path_to_json, 'w')
        rapidjson.dump(json_data, json_out)
        json_out.close()
        print("Done.")
    except Exception as e:
        print("Failed. {}.".format(e))


# Load JSON files
def load_json(path_to_json):
    """
    :param path_to_json: [str] local file path
    :return: the json data retrieved
    """
    json_in = open(path_to_json, 'r')
    data = rapidjson.load(json_in)
    json_in.close()
    if isinstance(data, str):
        data = rapidjson.loads(data)
    return data


# ====================================================================================================================
""" Misc """


# Download and show progress
def download(url, path_to_file, wait_to_retry=3600):
    """
    Reference: https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
    :param url: [str]
    :param path_to_file: [str]
    :param wait_to_retry: [int; float]
    :return:
    """
    r = requests.get(url, stream=True)  # Streaming, so we can iterate over the response

    if r.status_code == 429:
        time.sleep(wait_to_retry)

    total_size = int(r.headers.get('content-length'))  # Total size in bytes
    block_size = 1024 * 1024
    wrote = 0

    directory = os.path.dirname(path_to_file)
    if not os.path.exists(directory):
        os.mkdir(directory)

    with open(path_to_file, 'wb') as f:
        for data in tqdm.tqdm(r.iter_content(block_size), total=total_size // block_size, unit='MB'):
            wrote = wrote + len(data)
            f.write(data)

    f.close()

    r.close()

    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")


# Make a dictionary with keys and values being shape_type (in OSM .shp file) and shapely.geometry, respectively
def osm_geom_types():
    shape_types = {'Point': shapely.geometry.Point,
                   'LineString': shapely.geometry.LineString,
                   'LinearRing': shapely.geometry.LinearRing,
                   'MultiLineString': shapely.geometry.MultiLineString,
                   'Polygon': shapely.geometry.Polygon,
                   'MultiPolygon': shapely.geometry.MultiPolygon,
                   'GeometryCollection': shapely.geometry.GeometryCollection}
    return shape_types


# Update a nested dictionary or similar mapping.
def update_nested_dict(source_dict, overrides):
    """
    Reference: https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth

    :param source_dict: [dict]
    :param overrides: [dict]
    :return:
    """

    for key, val in overrides.items():
        if isinstance(val, collections.Mapping):
            source_dict[key] = update_nested_dict(source_dict.get(key, {}), val)
        elif isinstance(val, list):
            source_dict[key] = (source_dict.get(key, []) + val)
        else:
            source_dict[key] = overrides[key]
    return source_dict


# Split a list into (evenly sized) chunks
def split_list(lst, no_chunks):
    """Yield successive n-sized chunks from a list
    Reference: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks

    """
    chunk_size = math.ceil(len(lst) / no_chunks)
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
