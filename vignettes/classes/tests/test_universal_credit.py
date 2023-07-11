from vignettes.classes import universal_credit, childcare, classes, housing


def test_uc_standard_allowance() -> None:
    for key in universal_credit.STANDARD_ALLOWANCES:
        assert universal_credit.calc_standard_allowance(key) == universal_credit.STANDARD_ALLOWANCES[key]


def test_uc_child_element_one_child() -> None:
    assert universal_credit.calc_child_element(1) == universal_credit.FIRST_CHILD


def test_uc_child_element_two_children() -> None:
    assert universal_credit.calc_child_element(2) == universal_credit.FIRST_CHILD + universal_credit.ADDITIONAL_CHILD


def test_uc_childcare_element() -> None:
    assert universal_credit.calc_uc_childcare(1, True, True) == childcare.SINGLE_CHILD


def test_uc_childcare_not_working() -> None:
    """ If someone doesn't work, they can't claim for childcare"""
    assert universal_credit.calc_uc_childcare(1, True, False) == 0


def test_calc_uc_taper_trivial() -> None:
    assert universal_credit.calc_uc_taper(0, universal_credit.WorkAllowances.NONE) == 0


def test_calc_uc_taper_nontrivial() -> None:
    allowance = universal_credit.WorkAllowances.HIGHER
    assert universal_credit.calc_uc_taper(1000, allowance) \
           == (1000 - universal_credit.WORK_ALLOWANCES[allowance]) * universal_credit.UC_TAPER_RATE


def test_uclcwra_true() -> None:
    assert universal_credit.calc_uclcwra(True) == universal_credit.LCWRA


def test_uclcwra_false() -> None:
    assert universal_credit.calc_uclcwra(False) == 0.0


def test_calc_uc_disabled_children_additions() -> None:
    c1 = classes.Person(10, "disabled", 0, 0)
    c2 = classes.Person(5, "severely_disabled", 0, 0)
    assert universal_credit.calc_uc_disabled_children_additions([c1, c2]) \
           == universal_credit.DISABLED_CHILD_ADDITIONS[classes.DisabilityStatus.DISABLED] \
           + universal_credit.DISABLED_CHILD_ADDITIONS[classes.DisabilityStatus.SEVERELY_DISABLED]


def test_lha_scunthorpe_flatshare() -> None:
    lha_rate_scunthorpe_flatshare = housing.HOUSING_COSTS["LHA"]["Scunthorpe"][classes.LHACategory.A]
    assert universal_credit.calc_lha("Scunthorpe", classes.LHACategory.A) == lha_rate_scunthorpe_flatshare


def test_lha_london_one_bed() -> None:
    lha_rate_london_one_bed = housing.HOUSING_COSTS["LHA"]["Central London"][classes.LHACategory.B]
    assert universal_credit.calc_lha("Central London", classes.LHACategory.B) == lha_rate_london_one_bed

# TODO - write some unit tests for the taper!


def test_uc_taper_no_income() -> None:
    assert universal_credit.calc_uc_taper(0, classes.WorkAllowances.LOWER) == 0
