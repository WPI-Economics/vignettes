
from .classes import Cost, Family, LHACategory

# These are 2020-21 LHA rates - may need to find a 2019-20 LHA lookup.

HOUSING_COSTS = {
    30: {
        "Central London": {
            LHACategory.A: 154.19,
            LHACategory.B: 295.49,
            LHACategory.C: 365.92,
            LHACategory.D: 441.86,
            LHACategory.E: 593.75,
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
    50: {
        "Central London": {
            LHACategory.A: 178.85,
            LHACategory.B: 334.62,
            LHACategory.C: 461.54,
            LHACategory.D: 587.31,
            LHACategory.E: 727.38,
        },
        "Norwich": {
            LHACategory.A: 99.92,
            LHACategory.B: 150.00,
            LHACategory.C: 173.08,
            LHACategory.D: 189.92,
            LHACategory.E: 323.08
        },
        "Scunthorpe": {
            LHACategory.A: 80.08,
            LHACategory.B: 92.31,
            LHACategory.C: 109.62,
            LHACategory.D: 126.92,
            LHACategory.E: 167.31
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
