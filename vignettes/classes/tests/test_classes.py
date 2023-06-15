
from vignettes.classes.classes import Person, Family, FamilyType, BenefitUnit
from vignettes.classes import tax


# Test Person class

def test_person_gross_income() -> None:
    p = Person(18, "not_disabled", 35, 10.0)
    assert p.gross_income == 350.0


def test_person_adult_indicator() -> None:
    p = Person(18, "not_disabled", 0, 0)
    assert p.adult


def test_person_adult_indicator_false() -> None:
    p = Person(17, "not_disabled", 0, 0)
    assert not p.adult


def test_person_income_tax_payable() -> None:
    p = Person(18, "not_disabled", 35, 10.0)
    assert p.income_tax_payable == tax.calc_income_tax(350)


def test_person_nics_payable() -> None:
    p = Person(18, "not_disabled", 35, 10.0)
    assert p.nics_payable == tax.calc_national_insurance_contributions(350)


def test_person_net_income() -> None:
    p = Person(18, "not_disabled", 35, 10.0)
    assert p.net_income == p.gross_income - p.income_tax_payable - p.nics_payable


# Test Family class

def test_family_type_single() -> None:
    p = Person(30, "not_disabled", 0, 0)
    f = Family(0, [p], "Central London", 30, False, "none", False)
    assert f.famtype == FamilyType.SINGLE


def test_family_type_couple() -> None:
    p1 = Person(30, "not_disabled", 0, 0)
    p2 = Person(21, "not_disabled", 0, 0)
    f = Family(0, [p1, p2], "Central London", 30, False, "none", False)
    assert f.famtype == FamilyType.COUPLE


def test_family_type_young_single() -> None:
    p = Person(24, "not_disabled", 0, 0)
    f = Family(0, [p], "Central London", 30, False, "none", False)
    assert f.famtype == FamilyType.YOUNG_SINGLE


def test_family_type_young_couple() -> None:
    p1 = Person(21, "not_disabled", 0, 0)
    p2 = Person(23, "not_disabled", 0, 0)
    f = Family(0, [p1, p2], "Central London", 30, False, "none", False)
    assert f.famtype == FamilyType.YOUNG_COUPLE


def test_identify_adults() -> None:
    p1 = Person(21, "not_disabled", 0, 0)
    p2 = Person(23, "not_disabled", 0, 0)
    p3 = Person(17, "not_disabled", 0, 0)
    f = Family(0, [p1, p2, p3], "Central London", 30, False, "none", False)
    assert (f.adults == [p1, p2]) and f.children == [p3]


def test_num_children_two() -> None:
    p1 = Person(21, "not_disabled", 0, 0)
    p2 = Person(23, "not_disabled", 0, 0)
    p3 = Person(17, "not_disabled", 0, 0)
    p4 = Person(11, "not_disabled", 0, 0)
    f = Family(0, [p1, p2, p3, p4], "Central London", 30, False, "none", False)
    assert f.num_children == 2


def test_num_children_one() -> None:
    p1 = Person(21, "not_disabled", 0, 0)
    p2 = Person(23, "not_disabled", 0, 0)
    p3 = Person(17, "not_disabled", 0, 0)
    f = Family(0, [p1, p2, p3], "Central London", 30, False, "none", False)
    assert f.num_children == 1

