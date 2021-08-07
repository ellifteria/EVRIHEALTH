federal_poverty_guidelines = {
    1: 12880,
    2: 17420,
    3: 21960,
    4: 26500,
    5: 31040,
    6: 35580,
    7: 40120,
    8: 44660
}

def calculate_threshold(household_size):
    threshold_extension = 0
    while household_size > 8:
        household_size -= 1
        threshold_extension += 4540
    return federal_poverty_guidelines[household_size] + threshold_extension

def determine_financially_indignant(household_size, estimated_annual_income):
    poverty_threshold = calculate_threshold(household_size)
    if estimated_annual_income <= poverty_threshold * 2:
        return 1.00
    return 0

def determine_medically_indignant(household_size, estimated_annual_income, balance_due):
    poverty_threshold = calculate_threshold(household_size)
    if estimated_annual_income <= poverty_threshold * 2.5:
        if balance_due / estimated_annual_income > 0.05:
            return 0.95
    elif estimated_annual_income <= poverty_threshold * 3:
        if balance_due / estimated_annual_income > 0.05:
            return 0.90
    elif estimated_annual_income <= poverty_threshold * 3.5:
        if balance_due / estimated_annual_income > 0.05:
            return 0.85
    elif estimated_annual_income <= poverty_threshold * 4:
        if balance_due / estimated_annual_income > 0.10:
            return 0.80
    elif estimated_annual_income <= poverty_threshold * 5:
        if balance_due / estimated_annual_income > 0.10:
            return 0.75
    return 0

def determine_tier2_medically_indignant(household_size, estimated_annual_income, balance_due):
    if estimated_annual_income > calculate_threshold(household_size) * 5:
        if balance_due >= estimated_annual_income:
            return 0.95
        elif balance_due >= estimated_annual_income * 0.8:
            return 0.90
        elif balance_due >= estimated_annual_income * 0.6:
            return 0.85
        elif balance_due >= estimated_annual_income * 0.4:
            return 0.80
        elif balance_due >= estimated_annual_income * 0.2:
            return 0.75
    return 0

def determine_catastrophic_medically_indignant(household_size, estimated_annual_income, balance_due):
    if balance_due > estimated_annual_income:
        if estimated_annual_income <= calculate_threshold(household_size) * 5:
            return 0.975
        else:
            return 0.95
    return 0