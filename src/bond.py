cash_flows = [
    4.5,  # nov 22
    4.5,  # may 23
    4.5 + 100.0,  # nov 23
]

ytm = 3.4175 / 100

discounts = [
    (1 + ytm) ** -0,  # nov 22
    (1 + ytm) ** -1,  # may 23
    (1 + ytm) ** -2,  # nov 23
]

print(f"€{sum(c * d for c, d in zip(cash_flows, discounts)):.3f}")
