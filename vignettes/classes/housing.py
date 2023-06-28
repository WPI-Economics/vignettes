
from vignettes.classes.classes import Cost, Family, LHACategory

# These are 2023-24 LHA rates (frozen since 2020-21)
# 30th percentiles are from the 12 months to September 2022
# 50th percentiles are from FYE 2023

HOUSING_COSTS = {
    "LHA": {
        "Central London": {
            LHACategory.A: 154.19,
            LHACategory.B: 295.49,
            LHACategory.C: 365.92,
            LHACategory.D: 441.86,
            LHACategory.E: 593.75,
        },
        "Southwark": {
            LHACategory.A: 136.50,
            LHACategory.B: 295.49,
            LHACategory.C: 365.92,
            LHACategory.D: 441.86,
            LHACategory.E: 585.70
        },
        "Norwich": {
            LHACategory.A: 82.85,
            LHACategory.B: 113.92,
            LHACategory.C: 138.08,
            LHACategory.D: 163.40,
            LHACategory.E: 218.63
        },
        "Scunthorpe": {
            LHACategory.A: 56.00,
            LHACategory.B: 74.79,
            LHACategory.C: 103.56,
            LHACategory.D: 111.62,
            LHACategory.E: 136.93
        }
    },
    "30": {
        "Central London": {
            LHACategory.A: 176.02,
            LHACategory.B: 393.99,
            LHACategory.C: 523.56,
            LHACategory.D: 747.95,
            LHACategory.E: 1068.76
        },
        "Southwark": {
            LHACategory.A: 140.73,
            LHACategory.B: 303.70,
            LHACategory.C: 368.22,
            LHACategory.D: 460.27,
            LHACategory.E: 636.33
        },
        "Norwich": {
            LHACategory.A: 87.41,
            LHACategory.B: 126.58,
            LHACategory.C: 149.59,
            LHACategory.D: 178.36,
            LHACategory.E: 240.49
        },
        "Scunthorpe": {
            LHACategory.A: 66.50,
            LHACategory.B: 92.05,
            LHACategory.C: 109.32,
            LHACategory.D: 132.33,
            LHACategory.E: 149.59
        }
    },
    "50": {
        "Central London": {
            LHACategory.A: 210.00,
            LHACategory.B: 485.08,
            LHACategory.C: 675.00,
            LHACategory.D: 926.08,
            LHACategory.E: 2467.38,
        },
        "Southwark": {
            LHACategory.A: 171.92,
            LHACategory.B: 346.15,
            LHACategory.C: 426.92,
            LHACategory.D: 530.77,
            LHACategory.E: 755.77
        },
        "Norwich": {
            LHACategory.A: 109.62,
            LHACategory.B: 158.77,
            LHACategory.C: 183.46,
            LHACategory.D: 201.92,
            LHACategory.E: 334.62
        },
        "Scunthorpe": {
            LHACategory.A: 82.62,
            LHACategory.B: 95.08,
            LHACategory.C: 121.15,
            LHACategory.D: 138.46,
            LHACategory.E: 181.15
        }
    }
}


class HousingCosts(Cost):

    def calculate_cost(self, family: Family) -> float:

        # Get information from family object
        housing_costs_status = family.housing_costs
        location = family.location
        lha_cat = family.lha_category

        # Lookup the given percentile in the given location
        return HOUSING_COSTS[housing_costs_status][location][lha_cat]
