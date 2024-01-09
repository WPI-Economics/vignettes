
from vignettes.classes.classes import Person, Benefit, Family, DisabilityStatus

# For adults, assume those who are severely disabled receive the higher rate for both elements
# And that those who are disabled receive the lower rate for both elements

# 2021/22 amounts

PIP_MOBILITY = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: 23.70,
    DisabilityStatus.SEVERELY_DISABLED: 62.55
}
PIP_DAILY_LIVING = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: 60.00,
    DisabilityStatus.SEVERELY_DISABLED: 89.60
}

# Similar approach for DLA for children.
DLA_MOBILITY = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: 23.70,
    DisabilityStatus.SEVERELY_DISABLED: 62.55
}
DLA_CARE = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: 23.70,
    DisabilityStatus.SEVERELY_DISABLED: 89.60
}

'''
PIP_MOBILITY = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: 26.90,
    DisabilityStatus.SEVERELY_DISABLED: 71.00
}
PIP_DAILY_LIVING = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: 68.10,
    DisabilityStatus.SEVERELY_DISABLED: 101.75
}

# Similar approach for DLA for children.
DLA_MOBILITY = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: 26.90,
    DisabilityStatus.SEVERELY_DISABLED: 71.00
}
DLA_CARE = {
    DisabilityStatus.NOT_DISABLED: 00.00,
    DisabilityStatus.DISABLED: 26.90,
    DisabilityStatus.SEVERELY_DISABLED: 101.75
}
'''

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
