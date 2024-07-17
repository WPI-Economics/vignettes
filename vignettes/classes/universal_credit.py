from typing import List
from vignettes.classes import housing, childcare
from vignettes.classes.classes import Person, Benefit, Cost, Family, LHACategory, WorkAllowances, FamilyType, \
    DisabilityStatus, UCDeductionCategories, LimitedCapacityForWork
from vignettes.utils.read_params import read_params

# Benefit amounts are read in from the parameter system file
benefit_system = read_params()

# Initialise these global variables, using the data from the parameter system file

# 2021-22 awards, with benefit floor applied and additional benefits for those with no expectations

##################################################################################
# Additional elements for anti-poverty guarantee #################################

#LCWRA_ADDITION = 9.06
LCWRA_ADDITION = {
    "Enabled": benefit_system["UC"]["APG"]["LCWRA_ADDITION"]["ENABLED"],
    "Value": benefit_system["UC"]["APG"]["LCWRA_ADDITION"]["VALUE"]
}
# False in the current welfare system
# Add to true to allow a BU with two disabled people to claim the LCWRA twice
'''
SECOND_LCWRA = {
    "Enabled": True,
    "Value": 64.24
}
'''
SECOND_LCWRA = {
    "Enabled": benefit_system["UC"]["APG"]["SECOND_LCWRA"]["ENABLED"],
    "Value": benefit_system["UC"]["APG"]["SECOND_LCWRA"]["VALUE"]
}
'''
YOUNG_CHILD_ADDITION = {
    "Enabled": True,
    "Value": 63.04,
    "Cutoff": 2
}
'''
YOUNG_CHILD_ADDITION = {
    "Enabled": benefit_system["UC"]["APG"]["YOUNG_CHILD_ADDITION"]["ENABLED"],
    "Value": benefit_system["UC"]["APG"]["YOUNG_CHILD_ADDITION"]["VALUE"],
    "Cutoff": benefit_system["UC"]["APG"]["YOUNG_CHILD_ADDITION"]["CUTOFF"]
}

# Might we also need an addition to the disabled child element? Investigate.
#DISABLED_CHILD_ADDITION_ADDITION = 9.18
DISABLED_CHILD_ADDITION_ADDITION = {
    "Enabled": benefit_system["UC"]["APG"]["DISABLED_CHILD_ADDITION_ADDITION"]["ENABLED"],
    "Value": benefit_system["UC"]["APG"]["DISABLED_CHILD_ADDITION_ADDITION"]["VALUE"]
}

#####################################################################################

'''
STANDARD_ALLOWANCES = {
    FamilyType.YOUNG_SINGLE: 88.62,
    FamilyType.SINGLE: 88.62,
    FamilyType.YOUNG_COUPLE: 152.54,
    FamilyType.COUPLE: 152.54
}
'''

STANDARD_ALLOWANCES = {
    FamilyType.YOUNG_SINGLE: benefit_system["UC"]["STANDARD_ALLOWANCE"]["YOUNG_SINGLE"],
    FamilyType.SINGLE: benefit_system["UC"]["STANDARD_ALLOWANCE"]["SINGLE"],
    FamilyType.YOUNG_COUPLE: benefit_system["UC"]["STANDARD_ALLOWANCE"]["YOUNG_COUPLE"],
    FamilyType.COUPLE: benefit_system["UC"]["STANDARD_ALLOWANCE"]["COUPLE"]
}

LCWRA = benefit_system["UC"]["LCWRA"]

if LCWRA_ADDITION["Enabled"]:
    LCWRA = LCWRA + LCWRA_ADDITION["Value"]

'''
DISABLED_CHILD_ADDITIONS = {
    DisabilityStatus.DISABLED: 29.74 + DISABLED_CHILD_ADDITION_ADDITION,
    DisabilityStatus.SEVERELY_DISABLED: 92.80
}
'''

DISABLED_CHILD_ADDITIONS = {
    DisabilityStatus.DISABLED: benefit_system["UC"]["DISABLED_CHILD_ADDITIONS"]["LOWER"],
    DisabilityStatus.SEVERELY_DISABLED: benefit_system["UC"]["DISABLED_CHILD_ADDITIONS"]["HIGHER"]
}

if DISABLED_CHILD_ADDITION_ADDITION["Enabled"]:
    DISABLED_CHILD_ADDITIONS[DisabilityStatus.DISABLED] = DISABLED_CHILD_ADDITIONS[DisabilityStatus.DISABLED] + DISABLED_CHILD_ADDITION_ADDITION["Value"]

WORK_ALLOWANCES = {
    WorkAllowances.NONE: 0,
    WorkAllowances.LOWER: benefit_system["UC"]["WORK_ALLOWANCES"]["LOWER"],
    WorkAllowances.HIGHER: benefit_system["UC"]["WORK_ALLOWANCES"]["HIGHER"]
}

UC_TAPER_RATE = benefit_system["UC"]["TAPER_RATE"]

FIRST_CHILD = benefit_system["UC"]["CHILDREN"]["FIRST_CHILD"]
ADDITIONAL_CHILD = benefit_system["UC"]["CHILDREN"]["ADDITIONAL_CHILD"]
TWO_CHILD_LIMIT = benefit_system["UC"]["CHILDREN"]["TWO_CHILD_LIMIT"]

MAX_DEDUCTION = benefit_system["UC"]["MAX_DEDUCTION"]

'''
# 2021-22 awards, with a benefit floor applied.

STANDARD_ALLOWANCES = {
    FamilyType.YOUNG_SINGLE: 88.62,
    FamilyType.SINGLE: 88.62,
    FamilyType.YOUNG_COUPLE: 152.54,
    FamilyType.COUPLE: 152.54
}

LCWRA = 79.30

DISABLED_CHILD_ADDITIONS = {
    DisabilityStatus.DISABLED: 29.74,
    DisabilityStatus.SEVERELY_DISABLED: 92.80
}

WORK_ALLOWANCES = {
    WorkAllowances.NONE: 0,
    WorkAllowances.LOWER: 67.62,
    WorkAllowances.HIGHER: 118.85
}

UC_TAPER_RATE = 0.55

FIRST_CHILD = 65.20
ADDITIONAL_CHILD = 54.71
TWO_CHILD_LIMIT = False

MAX_DEDUCTION = 0.25

'''
'''
# All awards in 2023-24 amounts

STANDARD_ALLOWANCES = {
    FamilyType.YOUNG_SINGLE: 67.41,
    FamilyType.SINGLE: 85.09,
    FamilyType.YOUNG_COUPLE: 105.81,
    FamilyType.COUPLE: 133.57
}

LCWRA = 90.01

DISABLED_CHILD_ADDITIONS = {
    DisabilityStatus.DISABLED: 33.76,
    DisabilityStatus.SEVERELY_DISABLED: 105.44
}

WORK_ALLOWANCES = {
    WorkAllowances.NONE: 0,
    WorkAllowances.LOWER: 87.40,
    WorkAllowances.HIGHER: 145.59
}

UC_TAPER_RATE = 0.55

FIRST_CHILD = 62.21
ADDITIONAL_CHILD = 62.21
TWO_CHILD_LIMIT = True

MAX_DEDUCTION = 0.25
'''

class UCStandardAllowance(Benefit):

    def calculate_award(self, family: Family) -> float:

        # Access family attributes
        family_type = family.famtype
        return calc_standard_allowance(family_type)


def calc_standard_allowance(family_type: FamilyType) -> float:
    """
    Calculate UC standard allowance. There are four possible rates, depending on whether the family is a couple or
    single, with lower rates for those under 25.
    :param family_type: A string describing the family type.
    :return: standard allowance entitlement (£ per week)
    """

    return STANDARD_ALLOWANCES[family_type]


class UCChildElement(Benefit):

    def calculate_award(self, family: Family) -> float:

        # Access family attributes
        number_of_children = family.num_children
        return calc_child_element(number_of_children)


def calc_child_element(num_children: int) -> float:
    """
    Calculate UC child allowances.
    :param num_children: the number of children in the family
    :return: child allowance entitlement (£ per week)
    """
    if num_children == 0:
        return 0.0
    elif num_children == 1:
        return FIRST_CHILD
    elif num_children > 1:
        if TWO_CHILD_LIMIT:
            return FIRST_CHILD + ADDITIONAL_CHILD
        else:
            return FIRST_CHILD + (num_children - 1) * ADDITIONAL_CHILD


class LocalHousingAllowance(Benefit):

    def calculate_award(self, family: Family) -> float:

        # Access family attributes
        location = family.location
        lha_category = family.lha_category
        return calc_lha(location, lha_category)


def calc_lha(location: str, lha_category: LHACategory) -> float:
    """
    Calculate local housing allowance. This will depend both on the location and the category of accommodation required.
    :param location:
    :param lha_category:
    :return:
    """

    return housing.HOUSING_COSTS["LHA"][location][lha_category]


class UCChildcare(Benefit):

    def calculate_award(self, family: Family) -> float:

        # Access family attributes
        num_children = family.num_children
        claims_childcare = family.claims_childcare
        working = bool(family.gross_income)

        return calc_uc_childcare(num_children, claims_childcare, working)


def calc_uc_childcare(num_children: int, claims_childcare: bool, working: bool) -> float:
    if claims_childcare & working:
        if num_children == 1:
            return childcare.SINGLE_CHILD
        elif num_children > 1:
            return childcare.MULTIPLE_CHILDREN
        else:
            return 0.0
    else:
        return 0.0


class UCLCWRA(Benefit):

    def calculate_award(self, family: Family) -> float:
        limited_capability_for_work = family.limited_capability_for_work
        return calc_uclcwra(limited_capability_for_work)


def calc_uclcwra(limited_capability_for_work: LimitedCapacityForWork) -> float:
    if limited_capability_for_work is LimitedCapacityForWork.INDIVIDUAL:
        return LCWRA
    elif limited_capability_for_work is LimitedCapacityForWork.COUPLE:
        if SECOND_LCWRA["Enabled"]:
            return LCWRA + SECOND_LCWRA["Value"]
        else:
            return LCWRA
    else:
        return 0.0


class UCDisabledChildAdditions(Benefit):

    def calculate_award(self, family: Family) -> float:

        disabled_children = [c for c in family.children if c.disabled]

        return calc_uc_disabled_children_additions(disabled_children)


def calc_uc_disabled_children_additions(disabled_children: List[Person]) -> float:
    award = 0.0
    for c in disabled_children:
        award += DISABLED_CHILD_ADDITIONS[c.disability]

    return award


class UCYoungChildAddition(Benefit):

    def calculate_award(self, family: Family) -> float:

        if family.num_children > 0:
            youngest_child = sorted(family.children, key=lambda x: x.age, reverse=False)[0]
            return calc_uc_young_child_addition(youngest_child)
        else:
            return 0.0


def calc_uc_young_child_addition(child: Person) -> float:
    if (child.age < YOUNG_CHILD_ADDITION["Cutoff"]) & (YOUNG_CHILD_ADDITION["Enabled"]):
        return YOUNG_CHILD_ADDITION["Value"]
    else:
        return 0.0


class UCTaper(Benefit):

    def calculate_award(self, family: Family) -> float:

        # Access family attributes
        net_income = family.net_income
        work_allowance = family.uc_work_allowance

        return -1 * calc_uc_taper(net_income, work_allowance)


def calc_uc_taper(net_income: float, work_allowance: WorkAllowances) -> float:
    """

    :param net_income:
    :param work_allowance:
    :return:
    """

    work_allowance = WORK_ALLOWANCES[work_allowance]

    return max((net_income - work_allowance) * UC_TAPER_RATE, 0)


class UniversalCredit(Benefit):
    universal_credit_elements = [
        UCStandardAllowance(),
        UCChildElement(),
        LocalHousingAllowance(),
        UCTaper(),
        UCChildcare(),
        UCLCWRA(),
        UCDisabledChildAdditions(),
        UCYoungChildAddition()
    ]

    def calculate_award(self, family: Family) -> float:

        summation = sum([element.calculate_award(family) for element in self.universal_credit_elements])
        return max(summation, 0)


class UniversalCreditDeduction(Cost):

    def calculate_cost(self, family: Family) -> float:
        uc_std_allowance = UCStandardAllowance().calculate_award(family)
        if family.uc_deduction == UCDeductionCategories.FULL:
            return uc_std_allowance * MAX_DEDUCTION
        else:
            return 0.0
