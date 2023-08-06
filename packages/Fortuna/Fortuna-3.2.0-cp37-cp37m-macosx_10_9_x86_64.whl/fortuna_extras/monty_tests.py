from Fortuna import *


some_list = [i for i in range(11)]

monty = QuantumMonty(some_list)

print("\nSamples of monty.flat_uniform():")
for _ in range(10):
    print(monty.flat_uniform())


print("\nQuantum Monty Methods:\n")
distribution_timer(monty.flat_uniform)
distribution_timer(monty.front_linear)
distribution_timer(monty.middle_linear)
distribution_timer(monty.back_linear)
distribution_timer(monty.quantum_linear)
distribution_timer(monty.front_gauss)
distribution_timer(monty.middle_gauss)
distribution_timer(monty.back_gauss)
distribution_timer(monty.quantum_gauss)
distribution_timer(monty.front_poisson)
distribution_timer(monty.middle_poisson)
distribution_timer(monty.back_poisson)
distribution_timer(monty.quantum_poisson)
distribution_timer(monty)  # default monty is monty.quantum_monty


print("\nLazy Cat: Functional, More General Form of QuantumMonty:\n")
distribution_timer(lazy_cat, some_list)  # default fn=random_index
distribution_timer(lazy_cat, some_list, fn=front_linear)
distribution_timer(lazy_cat, some_list, fn=middle_linear)
distribution_timer(lazy_cat, some_list, fn=back_linear)
distribution_timer(lazy_cat, some_list, fn=quantum_linear)
distribution_timer(lazy_cat, some_list, fn=front_gauss)
distribution_timer(lazy_cat, some_list, fn=middle_gauss)
distribution_timer(lazy_cat, some_list, fn=back_gauss)
distribution_timer(lazy_cat, some_list, fn=quantum_gauss)
distribution_timer(lazy_cat, some_list, fn=front_poisson)
distribution_timer(lazy_cat, some_list, fn=middle_poisson)
distribution_timer(lazy_cat, some_list, fn=back_poisson)
distribution_timer(lazy_cat, some_list, fn=quantum_poisson)
distribution_timer(lazy_cat, some_list, fn=quantum_monty)


print("\nStatic Slicing:")
monty = QuantumMonty(some_list[:5])           # this copies data
distribution_timer(monty.flat_uniform)        # ranges from the front
monty = QuantumMonty(some_list[-5:])          # must recreate to use a different slice, copies data again.
distribution_timer(monty.flat_uniform)        # ranges from the back


print("\nDynamic Slicing:")                   # this does not copy data
distribution_timer(lazy_cat, some_list, 5)    # equivalent to
distribution_timer(lazy_cat, some_list[:5])   # ranges from the front
distribution_timer(lazy_cat, some_list, -5)   # new slice, no copy, equivalent to
distribution_timer(lazy_cat, some_list[-5:])  # ranges from the back


print("\nLazy Cat with custom ZeroCool method:")


def zero_cool_by_2(x):
    return random_range(x, step=2)


distribution_timer(zero_cool_by_2, 11)   # -> [0, 10] by 2
distribution_timer(zero_cool_by_2, -11)  # -> [-11, -1] by 2
# the above code shows that `zero_cool_by_2(x)` is ZeroCool compliant.

distribution_timer(lazy_cat, some_list, fn=zero_cool_by_2)  # -> [0, 10] by 2, values of some_list
