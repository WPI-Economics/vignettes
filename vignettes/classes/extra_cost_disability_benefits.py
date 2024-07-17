
from vignettes.classes.classes import Person, Benefit, Family, DisabilityStatus
from vignettes.utils.read_params import read_params

# For adults, assume those who are severely disabled receive the higher rate for both elements
# And that those who are disabled receive the lower rate for both elements

# Benefit amounts are read in from the parameter system file
benefit_system = read_params()

# Initialise these global variables, using the data from the parameter system file
PIP_MOBILITY = {
    DisabilityStatus.NOT_DISABLED: 0.00,
    DisabilityStatus.DISABLED: benefit_system["PIP"]["MOBILITY"]["STANDARD"],
    DisabilityStatus.SEVERELY_DISABLED: benefit_system["PIP"]["MOBILITY"]["ENHANCED"]
}
PIP_DAILY_LIVING = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: benefit_system["PIP"]["DAILY"]["STANDARD"],
    DisabilityStatus.SEVERELY_DISABLED: benefit_system["PIP"]["DAILY"]["ENHANCED"]
}

# Similar approach for DLA for children.
DLA_MOBILITY = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: benefit_system["DLA_CHILD"]["MOBILITY"]["LOWER"],
    DisabilityStatus.SEVERELY_DISABLED: benefit_system["DLA_CHILD"]["MOBILITY"]["HIGHER"]
}
DLA_CARE = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: benefit_system["DLA_CHILD"]["CARE"]["MIDDLE"],
    DisabilityStatus.SEVERELY_DISABLED: benefit_system["DLA_CHILD"]["CARE"]["HIGHEST"]
}


class PIP(Benefit):

    def calculate_award(self, family: Family) -> float:

        costs = 0.0
        for p in family.people:
            if p.adult:
                mobility = PIP_MOBILITY[p.disability]
                daily_living = PIP_DAILY_LIVING[p.disability]
                costs += (mobility + daily_living)

        return costs


class DLA(Benefit):

    def calculate_award(self, family: Family) -> float:

        costs = 0.0
        for p in family.people:
            if ~p.adult:
                mobility = DLA_MOBILITY[p.disability]
                care = DLA_CARE[p.disability]
                costs += (mobility + care)

        return costs
