from typing import List
from vignettes.classes import housing, childcare
from vignettes.classes.classes import Person, Benefit, Family, LHACategory, WorkAllowances, FamilyType, DisabilityStatus


# All awards in 2019-20 amounts

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

    return housing.HOUSING_COSTS[30][location][lha_category]


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


def calc_uclcwra(limited_capability_for_work: bool) -> float:
    if limited_capability_for_work:
        return LCWRA
    else:
        return 0.0


class UCDisabledChildAdditions(Benefit):

    def calculate_award(self, family: Family) -> float:

        disabled_children = [ c for c in family.children if c.disabled ]

        return calc_uc_disabled_children_additions(disabled_children)


def calc_uc_disabled_children_additions(disabled_children: List[Person]) -> float:
    award = 0.0
    for c in disabled_children:
        award += DISABLED_CHILD_ADDITIONS[c.disability]

    return award


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
        UCDisabledChildAdditions()
    ]

    def calculate_award(self, family: Family) -> float:

        summation = sum([element.calculate_award(family) for element in self.universal_credit_elements])
        return max(summation, 0)
