from vignettes.classes.equivalisation import FIRST_ADULT, ADDITIONAL_ADULT, OVER_14, UNDER_14
from vignettes.classes.classes import Person, Family


def test_equiv_couple() -> None:
    p1 = Person(30, "not_disabled", 0, 0)
    p2 = Person(30, "not_disabled", 0, 0)
    f = Family(0, [p1, p2], "Central London", "LHA", False, "no_costs", False, "default")
    assert f.calc_equivalisation_factor() == FIRST_ADULT + ADDITIONAL_ADULT


def test_equiv_single() -> None:
    p1 = Person(30, "not_disabled", 0, 0)
    f = Family(0, [p1], "Central London", "LHA", False, "no_costs", False, "default")
    assert f.calc_equivalisation_factor() == FIRST_ADULT


def test_equiv_couple_one_child_under14() -> None:
    p1 = Person(30, "not_disabled", 0, 0)
    p2 = Person(30, "not_disabled", 0, 0)
    p3 = Person(13, "not_disabled", 0, 0)
    f = Family(0, [p1, p2, p3], "Central London", "LHA", False, "no_costs", False, "default")
    assert f.calc_equivalisation_factor() == FIRST_ADULT + ADDITIONAL_ADULT + UNDER_14


def test_equiv_couple_one_child_over14() -> None:
    p1 = Person(30, "not_disabled", 0, 0)
    p2 = Person(30, "not_disabled", 0, 0)
    p3 = Person(14, "not_disabled", 0, 0)
    f = Family(0, [p1, p2, p3], "Central London", "LHA", False, "no_costs", False, "default")
    assert f.calc_equivalisation_factor() == FIRST_ADULT + ADDITIONAL_ADULT + OVER_14


def test_equiv_lone_parent() -> None:
    p1 = Person(30, "not_disabled", 0, 0)
    p2 = Person(14, "not_disabled", 0, 0)
    f = Family(0, [p1, p2], "Central London", "LHA", False, "no_costs", False, "default")
    assert f.calc_equivalisation_factor() == FIRST_ADULT + OVER_14
