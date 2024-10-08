import os
from getpass import getuser

username = getuser()

fullname_lkup = {
    "EdwardMcPherson": "Edward McPherson",
    "MatthewTibbles": "Matthew Tibbles",
    "EoghanMcCauley": "Eoghan McCauley"
}

DROPBOX_ROOT = fr"C:\Users\{username}\WPI Economics Dropbox\{fullname_lkup[username]}"

LOGGING_DIR = os.path.join(DROPBOX_ROOT, r"WPI team folder\CSPS\Legatum - poverty work\LI Policy Simulator\Vignettes\Logging")

PATH = os.path.join(DROPBOX_ROOT, r"WPI team folder\CSPS\Legatum - poverty work\LI Policy Simulator\Vignettes\vignette_list.xlsx")

PARAM_PATH = os.path.join(DROPBOX_ROOT, r"WPI team folder\CSPS\Legatum - poverty work\LI Policy Simulator\Vignettes\parameter_systems\benefit_floor_apg_2022_23.json")

OUT_DIR = os.path.join(DROPBOX_ROOT, r"WPI team folder\CSPS\Legatum - poverty work\LI Policy Simulator\Vignettes\output")