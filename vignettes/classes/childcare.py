
from .classes import Family, Cost, ChildcareCostCategories

SINGLE_CHILD = 149
MULTIPLE_CHILDREN = 256


class Childcare(Cost):

    def calculate_cost(self, family: Family) -> float:

        # Get information from family object
        childcare_costs = family.childcare_costs
        num_children = family.num_children

        if childcare_costs == ChildcareCostCategories.NONE:
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
