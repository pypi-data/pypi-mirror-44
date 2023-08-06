#cython: cdivision=True

from libc.stdint cimport uint8_t, uint64_t
from libc.string cimport memset
from cpython.mem cimport PyMem_Malloc, PyMem_Free

cdef int _bit_num = 8

cdef void _setBit(uint8_t data[], uint64_t n, int value = 1):
    cdef uint64_t index = n / _bit_num
    cdef int bit = n % _bit_num
    if value == 0:
        data[index] = (data[index]) & (~(1 << bit))
    else:
        data[index] = (data[index]) | (1 << bit)

cdef uint64_t _getBit(uint8_t data[], uint64_t n):
    cdef uint64_t index = n / _bit_num
    cdef int bit = n % _bit_num
    return data[index] & (1 << bit)

cdef class Bitmap:

    cdef uint8_t *data

    def __cinit__(self, uint64_t size):
        cdef uint64_t nsize = size / _bit_num + 1
        self.data = <uint8_t *>PyMem_Malloc(nsize)
        memset(self.data, 0, nsize)
        print('Alloc bitmap done')

    def __dealloc__(self):
        PyMem_Free(self.data)
        print('Free bitmap done')

class Prime:

    def __init__(self, end):
        self.end = end
        self.count = 0
        self.bitmap = Bitmap(end)
        self.done = False

    def cal(self):
        cdef uint64_t i = 2;
        cdef uint64_t j = 0;
        cdef uint64_t count = 0
        cdef uint64_t end = self.end
        cdef Bitmap bitmap = self.bitmap
        cdef uint8_t *data = bitmap.data

        _setBit(data, 0)
        _setBit(data, 1)

        while i < end + 1:
            if _getBit(data, i) == 0:
                count += 1
                j = 2 * i
                while j < end + 1:
                    _setBit(data, j)
                    j += i
            i += 1
        self.count = count
        self.done = True
        print('There are %d prime numbers in [0, %d]' % (count, end))

    def isPrime(self, n):
        if not self.done:
            raise Exception('Call cal method before this')
        if n > self.end:
            raise Exception('%d is lager than end %d' % (n, self.end))

        cdef Bitmap bitmap = self.bitmap
        cdef uint8_t *data = bitmap.data

        return _getBit(data, n) == 0

    def listPrime(self, start, end):
        if not self.done:
            raise Exception('Call cal method before this')
        if end > self.end:
            raise Exception('%d is lager than end %d' % (end, self.end))
        if start < 0:
            start = 0

        cdef Bitmap bitmap = self.bitmap
        cdef uint8_t *data = bitmap.data

        result = []

        for i in range(start, end + 1):
            if _getBit(data, i) == 0:
                result.append(i)

        return result


