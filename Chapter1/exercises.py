import time
from fibonacci import fib4
from functools import lru_cache
from sys import getsizeof
from math import log2, ceil

"""
Ex. 1

Improved Fibonacci generator
"""


def timer(func):

    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time() - t1
        print(f"{func.__name__} ran in {t2} seconds")

    return wrapper


@lru_cache(maxsize=None)
def better_fib(index):
    """
    Generates Fibonacci Numbers

    :param index: the nth number in the seres
    :return: the nth index in the seres
    """
    if index == 0:
        return 0, 1
    else:
        a, b = better_fib(index // 2)
        c = a * (b * 2 - a)
        d = a * a + b * b
        if index % 2 == 0:
            return c, d
        else:
            return d, c + d


@timer
def call_better_fib(index):
    return better_fib(index)[0]


@timer
def call_normal_fib(index):
    return fib4(index)


def exercise_1():
    """
    A faster (the fastest?) Fibonacci Sequence generator.

    Approx 650x faster then fib4, at reasonable indexes
        (000.245us Vs 155.382us at i = 1,000)

    Approx 44,650x faster at i = 10,000
    """
    i = 10000
    print(f"Index {i}")
    call_better_fib(i)
    call_normal_fib(i)


"""
Ex. 2

Int Wrapper for compression
"""

# def compress(func):

#     def wrapper(*args, **kwargs):
#         func(*args, **kwargs)

#     return wrapper


class BitStringCompression:
    def __init__(self, string):
        self.data = string

    def __str__(self):
        return self.data

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        # for i in range(0, self._data.bit_length() - 1, self._shift):  # -1 to exclude sentinal Val
        bits = self._data >> self.i & (pow(2, self._shift) - 1)  # gets 2 bits at a time
        g = self._unique_parts[bits]
        self.i += self._shift
        if self.i >= self._data.bit_length():
            raise StopIteration
        return g

    @property
    def data(self):
        g = ""
        for i in range(
            0, self._data.bit_length() - 1, self._shift
        ):  # -1 to exclude sentinal Val
            bits = self._data >> i & (pow(2, self._shift) - 1)  # gets 2 bits at a time
            g += self._unique_parts[bits]
        return g[::-1]  # [::-1] reverses the string by slicing backwards

    @data.setter
    def data(self, val):
        self._unique_parts = list({x for x in val})
        self._shift = ceil(log2(len(self._unique_parts)))
        bit_string = 1  # start with a sentinel
        for part in val:
            bit_string <<= self._shift
            bit_string |= self._unique_parts.index(part)
        self._data = bit_string


def exercise_2():
    original = "TAGCGATTTATA" * 1000
    print(f"Original is {getsizeof(original)} Bytes")
    compressed = BitStringCompression(original)
    print(f"Compressed is {getsizeof(compressed._data)} Bytes")
    print(f"Original and Compressed are the same: {original == compressed.data}")
    # print("Iteration:")
    # for i, letter in enumerate(compressed):
    #     print(letter)


"""
Ex. 3

Towers of Hanoi with n-towers.
"""


def exercise_3():
    pass


if __name__ == "__main__":
    print("-------- Ex. 1: --------")
    exercise_1()
    print("-------- Ex. 2: --------")
    exercise_2()
    print("-------- Ex. 3: --------")
    exercise_3()
