import timeit
import numpy as np
import pyximport; pyximport.install(language_level=3)
import test_python
import test_numpy
import test_cython
import test_c

a = [float(v) for v in range(1000000)]
b = np.arange(1e6)

# python
print(timeit.timeit(test_python.test(a)))

# Numpy
print(timeit.timeit(test_numpy.test(b)))

# Cython - naive
print(timeit.timeit(test_cython.test(b)))

# Cython calling C
print(timeit.timeit(test_c.test(b)))
