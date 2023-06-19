
from vignettes.classes.classes import Family, Person, Cost, DisabilityCostCategories
from vignettes.classes.extra_cost_disability_benefits import PIP, DLA

# Mapping from cost categories to the actual required multiplier.
DISCOST_MULTIPLIER = {
    DisabilityCostCategories.NONE: 0.0,
    DisabilityCostCategories.DEFAULT: 1.0,
    DisabilityCostCategories.ADDITIONAL: 1.2
}


class CostsOfDisability(Cost):

    def calculate_cost(self, family: Family) -> float:

        pip_award = PIP().calculate_award(family)
        dla_award = DLA().calculate_award(family)

        return (pip_award + dla_award) * DISCOST_MULTIPLIER[family.disability_costs]
