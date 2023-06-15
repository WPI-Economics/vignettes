from vignettes.classes.child_benefit import calc_child_benefit, ChildBenefit, FIRST_CHILD, ADDITIONAL_CHILD
from vignettes.classes.classes import Person, Family


def test_child_benefit_one_child() -> None:
    assert calc_child_benefit(1) == FIRST_CHILD


def test_child_benefit_two_children() -> None:
    assert calc_child_benefit(2) == FIRST_CHILD + ADDITIONAL_CHILD


def test_child_benefit_three_children() -> None:
    assert calc_child_benefit(3) == FIRST_CHILD + ADDITIONAL_CHILD * 2


def test_child_benefit_object() -> None:
    p1 = Person(30, "not_disabled", 0, 0)
    p2 = Person(30, "not_disabled", 0, 0)
    p3 = Person(14, "not_disabled", 0, 0)
    f = Family(0, [p1, p2, p3], "Central London", 30, False, "none", False)

    ben = ChildBenefit()

    assert ben.calculate_award(f) == FIRST_CHILD
