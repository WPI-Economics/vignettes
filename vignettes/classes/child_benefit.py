
from vignettes.classes.classes import Benefit, Family
from vignettes.utils.read_params import read_params

# Benefit amounts are read in from the parameter system file
benefit_system = read_params()

# Initialise these global variables, using the data from the parameter system file
FIRST_CHILD = benefit_system["CHILD_BENEFIT"]["FIRST_CHILD"]
ADDITIONAL_CHILD = benefit_system["CHILD_BENEFIT"]["ADDITIONAL_CHILD"]


class ChildBenefit(Benefit):

    def calculate_award(self, family: Family) -> float:

        # Get information from family object
        # Maybe this should be done with a getter rather than directly accessing the attribute?
        number_of_children = family.num_children

        return calc_child_benefit(number_of_children)


def calc_child_benefit(num_children: int) -> float:
    """
    Calculate the entitlement to child benefit. This depends only on the number of children and the rates.
    We are not currently modelling High Income Child Benefit Tax Charge
    :param num_children: The number of children in the family (int)
    :return: child benefit entitlement
    """

    if num_children == 0:
        return 0.0
    elif num_children == 1:
        return FIRST_CHILD
    elif num_children > 1:
        return FIRST_CHILD + (num_children - 1) * ADDITIONAL_CHILD
