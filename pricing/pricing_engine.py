import numpy as np

def elasticity_demand(Q0: float, P: float, P0: float, epsilon: float) -> float:
    """
    Predicts demand at a new price, given baseline demand at the original price.
    """
    return Q0 * (P / P0) ** (-epsilon)


def time_decay_discount(t_remaining: float, tau: float, D_max: float, alpha: float) -> float:
    """
    Calculates the discount rate (as a fraction, e.g. 0.25 = 25% off) based on
    how many days remain before expiry.
    """
    t_remaining = max(0, min(t_remaining, tau))  # clamp so we never go outside [0, tau]
    return D_max * (1 - t_remaining / tau) ** alpha


def recommended_price(original_price: float, t_remaining: float, tau: float,
                       D_max: float = 0.5, alpha: float = 1.0) -> float:
    """
    Combines the discount into an actual suggested shelf price.
    """
    discount = time_decay_discount(t_remaining, tau, D_max, alpha)
    return round(original_price * (1 - discount), 2)


if __name__ == "__main__":
    # Quick manual test — bread, 4-day shelf life, original price $2.80
    original_price = 2.80
    tau = 4

    print("Bread (4-day shelf life, $2.80 original price):")
    for days_left in [4, 3, 2, 1, 0]:
        price = recommended_price(original_price, days_left, tau, D_max=0.5, alpha=1.2)
        print(f"  {days_left} days left -> recommended price: ${price}")