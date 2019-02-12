cimport numpy as np

cdef extern from "std_dev.h":
    double std_dev(double *arr, size_t siz)

def test(np.ndarray[np.float64_t, ndim=1] a):
    return std_dev(<double*> a.data, a.size)