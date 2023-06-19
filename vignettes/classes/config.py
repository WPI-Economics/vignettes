
from vignettes.classes.universal_credit import UniversalCredit
from vignettes.classes.child_benefit import ChildBenefit
from vignettes.classes.housing import HousingCosts
from vignettes.classes.childcare import Childcare

BENEFITS = [
    ChildBenefit(),
    UniversalCredit()
]

COSTS = [
    HousingCosts(),
    Childcare()
]
