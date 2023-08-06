from Fortuna import FlexCat, distribution_timer


some_matrix = {
    "A": [lambda: 1, lambda: 2, lambda: 3, lambda: 4],
    "B": [10, 20, 30, 40],
    "C": [100, 200, 300, 400],
}

zero_cool_dispatch = (
    "front_linear", "middle_linear", "back_linear", "quantum_linear",
    "front_gauss", "middle_gauss", "back_gauss", "quantum_gauss",
    "front_poisson", "middle_poisson", "back_poisson", "quantum_poisson",
    "quantum_monty", "flat_uniform"
)


if __name__ == "__main__":
    print("\nFlexCat Test Suite\n")

    for v_bias in zero_cool_dispatch:
        for k_bias in zero_cool_dispatch:
            flex_cat = FlexCat(some_matrix, key_bias=k_bias, val_bias=v_bias)
            distribution_timer(flex_cat, label=f"FlexCat(some_matrix, key_bias='{k_bias}', val_bias='{v_bias}')")

    for v_bias in zero_cool_dispatch:
        flex_cat = FlexCat(some_matrix, val_bias=v_bias)
        for cat in tuple(some_matrix.keys()):
            distribution_timer(flex_cat, cat_key=cat, label=f"FlexCat(some_matrix, val_bias='{v_bias}')")
