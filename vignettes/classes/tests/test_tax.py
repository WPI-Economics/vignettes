from vignettes.classes import tax


def test_income_tax_higher_threshold() -> None:
    assert tax.calc_income_tax(tax.HIGHER_THRESHOLD) == (tax.HIGHER_THRESHOLD - tax.PERSONAL_ALLOWANCE) * tax.BASIC_RATE


def test_income_tax_additional_threshold() -> None:
    assert tax.calc_income_tax(tax.ADDITIONAL_THRESHOLD) \
           == (tax.HIGHER_THRESHOLD - tax.PERSONAL_ALLOWANCE) * tax.BASIC_RATE \
           + (tax.ADDITIONAL_THRESHOLD - tax.HIGHER_THRESHOLD) * tax.HIGHER_RATE


def test_nics_upper_earnings_limit() -> None:
    assert tax.calc_national_insurance_contributions(tax.UPPER_EARNINGS_LIMIT) \
           == (tax.UPPER_EARNINGS_LIMIT - tax.PRIMARY_THRESHOLD) * tax.BASIC_NIC_RATE
