
from .universal_credit import UniversalCredit
from .child_benefit import ChildBenefit
from .housing import HousingCosts
from .childcare import Childcare

BENEFITS = [
    ChildBenefit(),
    UniversalCredit()
]

COSTS = [
    HousingCosts(),
    Childcare()
]
