from typing import List
import pandas as pd
from datetime import datetime as dt
import logging

from vignettes.classes import config
from vignettes.classes.classes import Person, Family, BenefitUnit
from vignettes.utils.log_setup import __setup_logger

LOGGING_DIR = r"C:\Users\EdwardMcPherson\WPI Economics Dropbox\Edward McPherson\WPI team folder\CSPS\Legatum - poverty " \
              r"work\LI Policy Simulator\Vignettes\Logging"

logger = logging.getLogger("vignettes")
logger.propagate = False
__setup_logger(logger, logging_dir=LOGGING_DIR)


def import_vignette_list(path: str) -> pd.DataFrame:
    # Read in as dataframe
    task_df = pd.read_excel(path, dtype={
        "childcare_costs": "str",
    })
    return task_df


def init_vignette_list(task_df: pd.DataFrame) -> List[BenefitUnit]:

    vignettes = task_df["vignette_number"].unique()

    vig_array = []
    for vig in vignettes:

        vig_df = task_df.loc[task_df["vignette_number"] == vig, :]

        if vig_df["location"].unique().__len__() == 1:
            vig_loc = vig_df["location"].unique()[0]
        else:
            raise ValueError("Family must be specified entirely in one location.")

        if vig_df["housing_costs_percentile"].unique().__len__() == 1:
            housing_costs_percentile = str(vig_df["housing_costs_percentile"].unique()[0])
        else:
            raise ValueError("Family must be specified with a single level of housing costs.")

        if vig_df["claims_housing"].unique().__len__() == 1:
            claims_housing = vig_df["claims_housing"].unique()[0]
        else:
            raise ValueError("Family can only exhibit a single type of claiming behaviour at a time.")

        if vig_df["childcare_costs"].unique().__len__() == 1:
            childcare_costs = vig_df["childcare_costs"].unique()[0]
        else:
            raise ValueError("Family must have a single level of childcare costs.")

        if vig_df["claims_childcare"].unique().__len__() == 1:
            claims_childcare = vig_df["claims_childcare"].unique()[0]
        else:
            raise ValueError("Family can only exhibit a single type of claiming behaviour at a time.")

        if vig_df["disability_costs"].unique().__len__() == 1:
            disability_costs = vig_df["disability_costs"].unique()[0]
        else:
            raise ValueError()

        if vig_df["uc_deduction"].unique().__len__() == 1:
            uc_deduction = vig_df["uc_deduction"].unique()[0]
        else:
            raise ValueError()

        records = vig_df.to_records()
        people_array = []
        for rec in records:
            p = Person(rec.age, rec.disabled, rec.hours, rec.wage_rate)
            people_array.append(p)

        f = Family(vig,
                   people_array,
                   vig_loc,
                   housing_costs_percentile,
                   claims_housing,
                   childcare_costs,
                   claims_childcare,
                   disability_costs,
                   uc_deduction
                   )

        bu = BenefitUnit(f,
                         config.BENEFITS,
                         config.COSTS,
                         )

        vig_array.append(bu)

    return vig_array


def output_vignette_outcomes(out_df: pd.DataFrame, out_path: str):
    out_df.to_excel(out_path, index=False)


def main():
    path = r"C:\Users\EdwardMcPherson\WPI Economics Dropbox\Edward McPherson\WPI team folder\CSPS\Legatum - poverty " \
           r"work\LI Policy Simulator\Vignettes\vignette_list.xlsx"

    # Import list of vignettes to do
    task_df = import_vignette_list(path)

    # Convert to vignettes
    vig_list = init_vignette_list(task_df)

    # Do each vignette
    poverty_status = dict()
    for vig in vig_list:
        poverty_status[vig.identity] = [vig.tra,
                                        # vig.get_poverty_lines()["minimum income standard"],
                                        # vig.get_poverty_status(vig.get_poverty_lines()["minimum income standard"]),
                                        vig.get_poverty_lines()["poverty line"],
                                        vig.get_poverty_status(vig.get_poverty_lines()["poverty line"]),
                                        vig.get_poverty_lines()["deep poverty line"],
                                        vig.get_poverty_status(vig.get_poverty_lines()["deep poverty line"]),
                                        ]

    # Convert to dataframe for output
    out_df = pd.DataFrame.from_dict(poverty_status,
                                    orient="index",
                                    columns=["TRA",
                                             # "Minimum Income Standard (MIS)",
                                             # "Below MIS",
                                             "Poverty Line",
                                             "In Poverty",
                                             "Deep Poverty Line",
                                             "In Deep Poverty"]
                                    ).reset_index().rename(columns={"index": "vignette_number"})

    # Merge back onto input detail
    merged_df = pd.merge(task_df,
                         out_df,
                         how="left",
                         on="vignette_number"
                         )

    timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = rf"C:\Users\EdwardMcPherson\WPI Economics Dropbox\Edward McPherson\WPI team folder\CSPS\Legatum - "\
               rf"poverty work\LI Policy Simulator\Vignettes\output\vignette_outcomes_{timestamp}.xlsx"

    output_vignette_outcomes(merged_df, out_path)


if __name__ == "__main__":
    main()
