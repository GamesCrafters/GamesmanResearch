# Pure Python
# python3 -m timeit -s "import test_python; import numpy as np; a = [float(v) for v in range(1000000)]" "test_python.test(a)"
# Numpy
# python3 -m timeit -s "import test_numpy; import numpy as np; a = np.arange(1e6)" "test_numpy.test(a)"
# Cython - naive
# python3 -m timeit -s "import pyximport; pyximport.install(language_level=3); import test_cython; import numpy as np; a = np.arange(1e6)" "test_cython.test(a)"
# Cython calling C
# python3 -m timeit -s "import test_c; import numpy as np; a = np.arange(1e6)"
python3 -m timeit -s "import pyximport; pyximport.install(); import test_c; import numpy as np; a = np.arange(1e6)" "test_c.cStdDev(a)"
