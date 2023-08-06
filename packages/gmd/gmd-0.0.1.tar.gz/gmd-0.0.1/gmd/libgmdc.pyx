#!python
#cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False

import cython
cimport numpy as np
import numpy
from libc.math cimport abs, ceil, pow
from libc.stdlib cimport rand, srand

ctypedef np.int32_t int32
ctypedef np.float64_t float64
ctypedef np.uint8_t uint8

cdef extern from "time.h":
    long int time(int)

def set_seed(seed):
    if seed is None:
        srand(time(0))
    else:
        srand(seed)

cdef int32 my_sum(uint8[:] view):
    cdef int32 i = 0, acc = 0
    for i in range(len(view)):
        acc += view[i]
    return acc

cpdef float64 kstest(uint8[:] view, int32[:] sorted_index):
    """
    Compute the Kolmogorov-Smirnov statistic on 2 samples. Assumes no ties.

    Parameters
    ----------
    view : 1-D array
        view is a logical array specifying the samples to include
    sorted_index : 1-D array
        the sorted Index

    Returns
    -------
    statistic : float
    """
    cdef float64 cum_dist = 0.0
    cdef float64 max_dist = 0.0
    cdef int32 remaining = my_sum(view)
    cdef int32 total = sorted_index.shape[0]

    cdef int32 i = 0
    for i in range(total):
        if view[sorted_index[i]]:
            cum_dist += 1.0/remaining
        current_diff = abs(((i + 1.0)/total) - cum_dist)
        if current_diff > max_dist:
            max_dist = current_diff
    return max_dist

cdef subspace_slice(int32[:,:] sorted_index, int32[:] subspaces, int32 reference_dim, float64 alpha):
    """
    Cuts a hypercube out of the full space and returns the contained data points.

    Parameters
    ----------
    subspaces : orthogonal projections defining the constraints of the hypercube
    reference_dim : the unconstrained projection

    Returns
    -------
    1-D array with the length of the object count. If 1 the object is in the cube, if 0 it isn't
    """
    cdef int32 rows = sorted_index.shape[0]
    cdef int32 slice_size = <int>ceil(rows * (pow(alpha, (1.0/(len(subspaces)-1)))))
    cdef uint8[:] selection = numpy.ones(rows, dtype=numpy.uint8)
    cdef int32 s, l, r, j, i
    for i in range(len(subspaces)):
        s = subspaces[i]
        if s != reference_dim:
            #l = numpy.random.randint(0, self.rows - slice_size)
            l = rand() % (rows - slice_size)
            r = l + slice_size
            for j in range(0, l):
                selection[sorted_index[j, s]] = 0
            for j in range(r, rows):
                selection[sorted_index[j, s]] = 0
    #return numpy.frombuffer(selection, dtype=numpy.uint8)
    return selection

cpdef avg_deviation(int32[:,:] sorted_index, int32[:] subspaces, int32 reference_dim, float64 alpha, int32 runs):
        """
        Compute the deviation in a subspace given the reference dimension.

        Parameters
        ----------
        subspaces : orthogonal projections defining the constraints of the hypercube
        reference_dim : the unconstrained projection

        Returns
        -------
        float with the deviation of the subspaces wrt. the reference_dim
        """
        cdef float64 result = 0.0
        cdef uint8[:] my_slice
        cdef int32[:] ref = sorted_index[:, reference_dim]
        for _ in range(runs):
            my_slice = subspace_slice(sorted_index, subspaces, reference_dim, alpha)
            result = result + kstest(my_slice, ref)
        return result/runs