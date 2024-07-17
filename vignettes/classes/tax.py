
from vignettes.utils.read_params import read_params

# Benefit amounts are read in from the parameter system file
benefit_system = read_params()

# Initialise these global variables, using the data from the parameter system file
PERSONAL_ALLOWANCE = benefit_system["INCOME_TAX"]["PERSONAL_ALLOWANCE"]
BASIC_RATE = benefit_system["INCOME_TAX"]["BASIC_RATE"]

HIGHER_THRESHOLD = benefit_system["INCOME_TAX"]["HIGHER_THRESHOLD"]
HIGHER_RATE = benefit_system["INCOME_TAX"]["HIGHER_RATE"]

ADDITIONAL_THRESHOLD = benefit_system["INCOME_TAX"]["ADDITIONAL_THRESHOLD"]
ADDITIONAL_RATE = benefit_system["INCOME_TAX"]["ADDITIONAL_RATE"]

# NICs - note that these are aligned to income tax thresholds
PRIMARY_THRESHOLD = benefit_system["NICS"]["PRIMARY_THRESHOLD"]
BASIC_NIC_RATE = benefit_system["NICS"]["BASIC_NIC_RATE"]
UPPER_EARNINGS_LIMIT = benefit_system["NICS"]["UPPER_EARNINGS_LIMIT"]
HIGHER_NIC_RATE = benefit_system["NICS"]["HIGHER_NIC_RATE"]

'''
# 2021-22 amounts
# Income Tax
PERSONAL_ALLOWANCE = 242
BASIC_RATE = 0.2

HIGHER_THRESHOLD = 967
HIGHER_RATE = 0.4

ADDITIONAL_THRESHOLD = 2885
ADDITIONAL_RATE = 0.45

# NICs - note that these are aligned to income tax thresholds
PRIMARY_THRESHOLD = 242
BASIC_NIC_RATE = 0.12
UPPER_EARNINGS_LIMIT = 967
HIGHER_NIC_RATE = 0.02
'''

'''
# Income Tax
PERSONAL_ALLOWANCE = 242
BASIC_RATE = 0.2

HIGHER_THRESHOLD = 967
HIGHER_RATE = 0.4

ADDITIONAL_THRESHOLD = 2407
ADDITIONAL_RATE = 0.45

# NICs - note that these are aligned to income tax thresholds
PRIMARY_THRESHOLD = 242
BASIC_NIC_RATE = 0.12
UPPER_EARNINGS_LIMIT = 967
HIGHER_NIC_RATE = 0.02
'''

# Note - we do not model the personal allowance clawback at £100,000 per annum


def calc_income_tax(gross_income: float) -> float:
    """
    Calculate the payable amount of income tax on a given gross income
    :param gross_income: individual gross income (£ per week)
    :return: income tax payable (£ per week)
    """
    if gross_income <= PERSONAL_ALLOWANCE:
        return 0

    if (gross_income > PERSONAL_ALLOWANCE) & (gross_income <= HIGHER_THRESHOLD):
        return (gross_income - PERSONAL_ALLOWANCE) * BASIC_RATE

    if (gross_income > HIGHER_THRESHOLD) & (gross_income <= ADDITIONAL_THRESHOLD):
        return (HIGHER_THRESHOLD - PERSONAL_ALLOWANCE) * BASIC_RATE + (gross_income - HIGHER_THRESHOLD) * HIGHER_RATE

    if gross_income > ADDITIONAL_THRESHOLD:
        return ((HIGHER_THRESHOLD - PERSONAL_ALLOWANCE) * BASIC_RATE
                + (ADDITIONAL_THRESHOLD - HIGHER_THRESHOLD) * HIGHER_RATE
                + (gross_income - ADDITIONAL_THRESHOLD) * ADDITIONAL_RATE)


def calc_national_insurance_contributions(gross_income: float) -> float:
    """
    Calculate the payable amount of NICs on a given gross income
    :param gross_income: individual gross income (£ per week)
    :return: NICs payable (£ per week)
    """
    if gross_income <= PRIMARY_THRESHOLD:
        return 0

    if (gross_income > PRIMARY_THRESHOLD) & (gross_income <= UPPER_EARNINGS_LIMIT):
        return (gross_income - PRIMARY_THRESHOLD) * BASIC_NIC_RATE

    if gross_income > UPPER_EARNINGS_LIMIT:
        return ((UPPER_EARNINGS_LIMIT - PRIMARY_THRESHOLD) * BASIC_NIC_RATE
                + (gross_income - UPPER_EARNINGS_LIMIT) * HIGHER_NIC_RATE)
