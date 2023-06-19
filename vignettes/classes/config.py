
from vignettes.classes.universal_credit import UniversalCredit
from vignettes.classes.child_benefit import ChildBenefit
from vignettes.classes.housing import HousingCosts
from vignettes.classes.childcare import Childcare
from vignettes.classes.extra_cost_disability_benefits import PIP, DLA
from vignettes.classes.costs_of_disability import CostsOfDisability

BENEFITS = [
    ChildBenefit(),
    UniversalCredit(),
    PIP(),
    DLA()
]

COSTS = [
    HousingCosts(),
    Childcare(),
    CostsOfDisability()
]
