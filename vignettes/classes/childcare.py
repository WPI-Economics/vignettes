
from vignettes.classes.classes import Family, Cost, ChildcareCostCategories
from vignettes.utils.read_params import read_params

# Benefit amounts are read in from the parameter system file
benefit_system = read_params()

# Initialise these global variables, using the data from the parameter system file
SINGLE_CHILD = benefit_system["UC"]["CHILDCARE"]["SINGLE_CHILD"],
MULTIPLE_CHILDREN = benefit_system["UC"]["CHILDCARE"]["MULTIPLE_CHILDREN"]


class Childcare(Cost):

    def calculate_cost(self, family: Family) -> float:

        # Get information from family object
        childcare_costs = family.childcare_costs
        num_children = family.num_children

        if childcare_costs == ChildcareCostCategories.NO_COSTS:
            return 0.0

        elif childcare_costs == ChildcareCostCategories.UC_THRESHOLD:
            if num_children == 0:
                return 0.0
            if num_children == 1:
                return SINGLE_CHILD
            elif num_children > 1:
                return MULTIPLE_CHILDREN

        elif childcare_costs == ChildcareCostCategories.ADDITIONAL:
            if num_children == 0:
                return 0.0
            if num_children == 1:
                return SINGLE_CHILD * 1.2
            elif num_children > 1:
                return MULTIPLE_CHILDREN * 1.2
