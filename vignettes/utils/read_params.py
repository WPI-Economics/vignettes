import json

from vignettes.utils import config

PARAM_PATH = config.PARAM_PATH


def read_params():

    with open(PARAM_PATH, "r") as f:
        config_dict = json.load(f)

    return config_dict
