import json

PARAM_PATH = r"C:\Users\EdwardMcPherson\WPI Economics Dropbox\Edward McPherson\WPI team folder\CSPS\Legatum - poverty " \
             r"work\LI Policy Simulator\Vignettes\parameter_systems\benefit_floor_apg_2022_23.json"

def read_params():

    with open(PARAM_PATH, "r") as f:
        config_dict = json.load(f)

    return config_dict
