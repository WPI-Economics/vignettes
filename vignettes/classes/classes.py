from abc import ABC, abstractmethod
from typing import List
from enum import Enum, auto

from vignettes.classes import tax, poverty_lines, equivalisation


class DisabilityStatus(Enum):
    NOT_DISABLED = auto()
    DISABLED = auto()
    SEVERELY_DISABLED = auto()


class IncorrectInputError(Exception):
    """ Custom error """


class Person:

    def __init__(self, age: int, disabled: str, hours: int, wage_rate: float):
        # Demographics
        self.age = age
        self.adult = (age >= 18)
        try:
            self.disability = DisabilityStatus[disabled.upper()]
        except KeyError:
            raise IncorrectInputError("Disability status must be one of: not_disabled, disabled, severely_disabled")

        self.disabled = self.disability != DisabilityStatus.NOT_DISABLED

        # Get gross income
        self.hours = hours
        self.wage_rate = wage_rate
        self.gross_income = hours * wage_rate

        # Get net income
        self.income_tax_payable = tax.calc_income_tax(self.gross_income)
        self.nics_payable = tax.calc_national_insurance_contributions(self.gross_income)
        self.net_income = self.gross_income - self.income_tax_payable - self.nics_payable


""" 
Want to get the Family object just to represent the demographic characteristitcs and income.
Then a BenefitUnit class can handle benefit awards, costs, etc. 
Should lead to better separation! 
"""


class LHACategory(Enum):
    """LHA Categories"""
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()


class WorkAllowances(Enum):
    """ Different possiblities for Work Allowances"""
    NONE = auto()
    LOWER = auto()
    HIGHER = auto()


class ChildcareCostCategories(Enum):
    """ Different options for childcare"""
    NO_COSTS = auto()
    UC_THRESHOLD = auto()
    ADDITIONAL = auto()


class DisabilityCostCategories(Enum):
    """ Different disability cost options"""
    NONE = auto()
    DEFAULT = auto()
    ADDITIONAL = auto()


class FamilyType(Enum):
    """ Different options for core family type"""
    YOUNG_SINGLE = auto()
    SINGLE = auto()
    YOUNG_COUPLE = auto()
    COUPLE = auto()


class Family:

    def __init__(self,
                 identity: int,
                 people: List[Person],
                 location: str,
                 housing_costs: int,
                 claims_housing: bool,
                 childcare_costs: str,
                 claims_childcare: bool,
                 disability_costs: str
                 ):

        # Set id
        self.identity = identity

        # Set family location
        self.location = location

        # list of Person objects
        self.people = people
        self.adults = [p for p in self.people if p.adult]
        self.children = [p for p in self.people if not p.adult]

        # Disability status
        self.disabled = any([p.disabled for p in self.people])
        self.limited_capability_for_work = any([adult.disabled for adult in self.adults])

        # Set claim status
        self.claims_housing = claims_housing
        self.claims_childcare = claims_childcare

        # Determine family type
        self.famtype = self.determine_family_type()
        self.num_children = len(self.children)
        self.lha_category = self.calc_lha_category()
        self.uc_work_allowance = self.calc_uc_work_allowance()

        # Get gross income
        self.gross_income = sum([p.gross_income for p in self.people])
        #  Get net income
        self.net_income = sum([p.net_income for p in self.people])

        # Set equivalisation
        self.equiv = self.calc_equivalisation_factor()

        # Set costs
        self.housing_costs = housing_costs
        self.childcare_costs = ChildcareCostCategories[childcare_costs.upper()]
        self.disability_costs = DisabilityCostCategories[disability_costs.upper()]

    def determine_family_type(self) -> FamilyType:

        num_adults = len(self.adults)

        if num_adults == 1:
            if self.adults[0].age < 25:
                return FamilyType.YOUNG_SINGLE
            else:
                return FamilyType.SINGLE
        if num_adults == 2:
            if all([(adult.age < 25) for adult in self.adults]):
                return FamilyType.YOUNG_COUPLE
            else:
                return FamilyType.COUPLE

    def calc_lha_category(self) -> LHACategory:
        """
        Set the LHA category of the family. This is an approximation - the real logic depends
        on the gender of the children, with different logic for those under 10.
        :return: A string representing the LHA category of the family.
        """
        if self.famtype in [FamilyType.SINGLE, FamilyType.YOUNG_SINGLE] and self.adults[0].age < 35:
            return LHACategory.A
        else:
            if self.num_children == 0:
                return LHACategory.B
            elif self.num_children == 1:
                return LHACategory.C
            elif self.num_children == 2:
                return LHACategory.D
            elif self.num_children > 2:
                return LHACategory.E

    def calc_uc_work_allowance(self) -> WorkAllowances:

        has_allowance = False
        if self.num_children > 0:
            has_allowance = True
        if self.limited_capability_for_work:
            has_allowance = True

        if has_allowance:
            # What do we do when entitlement to one benefit depends on receipt of another?
            # Cannot work out the entitlement as a clean function of income / demographics.
            if self.claims_housing:
                return WorkAllowances.LOWER
            else:
                return WorkAllowances.HIGHER
        else:
            return WorkAllowances.NONE

    def calc_equivalisation_factor(self) -> float:

        num_adults = len(self.adults)

        # Adults
        if num_adults > 0:
            equiv = equivalisation.FIRST_ADULT + equivalisation.ADDITIONAL_ADULT * (num_adults - 1)
        else:
            raise ValueError("Each family should have at least one adult.")

        # Children
        under_14s = len([c for c in self.children if c.age < 14])
        over_14s = len([c for c in self.children if c.age > 13])
        equiv += equivalisation.UNDER_14 * under_14s + equivalisation.OVER_14 * over_14s

        return equiv


class Benefit(ABC):
    """Abstract class representing a benefit award for a Family"""

    @abstractmethod
    def calculate_award(self, family: Family) -> float:
        """Compute the amount of award for a given Family"""


class Cost(ABC):
    """Abstract class representing a cost facing a family"""

    @abstractmethod
    def calculate_cost(self, family: Family) -> float:
        """Compute the cost for a given BenefitUnit"""


class BenefitUnit:

    def __init__(self, family: Family, benefits: List[Benefit], costs: List[Cost]):
        self.family = family
        self.benefits = benefits
        self.costs = costs

        # Set identity (based on identity of family)
        self.identity = self.family.identity

        # Calculate total benefit award
        self.total_award = self.calculate_total_award()

        # Calculate total costs
        self.total_costs = self.calculate_total_costs()

        # Get total income from family
        self.net_income = self.family.net_income

    def calculate_total_award(self) -> float:
        total_award = 0
        for ben in self.benefits:
            total_award += ben.calculate_award(self.family)

        return total_award

    def calculate_total_costs(self) -> float:
        total_costs = 0
        for cost in self.costs:
            cost_amount = cost.calculate_cost(self.family)
            total_costs += cost_amount

        return total_costs

    def get_poverty_lines(self) -> dict:
        return {"minimum income standard": poverty_lines.MIS_COUPLE * self.family.equiv,
                "poverty line": poverty_lines.EQ_POV_LINE * self.family.equiv,
                "deep poverty line": poverty_lines.EQ_DEEP_POV_LINE * self.family.equiv
                }

    def get_total_resources_available(self) -> float:
        return max(self.net_income + self.total_award - self.total_costs, 0)

    def get_poverty_status(self, poverty_line: float) -> bool:
        return (self.net_income + self.total_award - self.total_costs) < poverty_line
