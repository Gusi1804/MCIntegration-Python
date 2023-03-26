import numpy as np  # used to generate the random x and y coordinates, as well as calculating the standard deviation and mean from a list
import math  # used to calculate a square root
import time  # used to take the runtime
import threading  # used to implement parallelization

def desc(func):
    if func == "n":
        return "e^(-x^2)"
    elif func == "p":
        return "Ax^n"
    elif func == "s":
        return "sin(x)"
    elif func == "c":
        return "cos(x)"
    elif func == "sqs":
        return "sqrt(sin(x))"
    elif func == "l":
        return "ln(x)"


def print_arr(arr):
    res = ""
    for el in arr:
        res += el + "\n"

    return res


def main_f():
    fs = ("n: e^(-x^2)", "p: Ax^n", "s: sin(x)", "sqs: sqrt(sin(x))", "c: cos(x)", "l: ln(x)")
    func = input(f"Select a function to integrate:\n{print_arr(fs)} ").strip()

    print(f"The function to integrate is {desc(func)}")

    if func == "p":
        A = float(input(f"Input the value of A: "))
        n = float(input(f"Input the value of n: "))
    else:
        A = 0
        n = 0

    N = int(input("Enter the value of N (number of repetitions): "))

    a = float(input("Enter the value of a: "))
    b = float(input("Enter the value of b: "))

    r_tot = 1000

    min = min_val(a, b, func, A, n)
    max = max_val(a, b, func, A, n)

    # print(min, max)

    start = time.time()  # start a chronometer to see how much time the simulation takes

    res = []  # list to store all the results

    for i in range(N): # repeat N times (i.e., generate n πs)
        p_in = 0  # variable that stores the points that were within the circle

        for m in range(r_tot):  # repeat for r_tot points (i.e., generate r_tot points)
            x = np.random.uniform(a, b)  # generate x coordinate
            y = np.random.uniform(min, max)  # generate y coordinate

            f_x = f(x, func, A, n)
            # print(x, f_x)
            # print(x, y)

            if y > 0 and y <= f_x:
                p_in += 1
            elif y < 0 and y <= f_x:
                p_in -= 1

        # print(f"ratio: {(p_pos - p_neg)/r_tot}")

        area = (b - a) * (max - min) * (p_in / r_tot)

        res.append(area)

    stdev = np.std(res,
                   ddof=1)  # calculate the standard deviation; important note: the 'ddof=1' parameter is used so that the standard deviation of a SAMPLE is calculated (i.e., the division of the differences of each value from the mean is divided by N-1), otherwise, the STDEV of the populations is calculated (i.e., the division of the differences of each value from the mean is divided by N).
    se = stdev / math.sqrt(N)  # calculate the standard error of the mean value
    mean = np.mean(res)  # calculate the mean
    end = time.time()  # save the endtime
    print(
        f'Mean: {mean}, Std. Dev.: {stdev}, Std. Err.: {se}, n: {N}, rTot: {r_tot}, t: {end - start}')  # print the results


def f(x, func, A, n):
    if func == "n":
        return np.exp(np.e, -1 * x * x)
    elif func == "p":
        return A * pow(x, n)
    elif func == "s":
        return np.sin(x)
    elif func == "c":
        return np.cos(x)
    elif func == "sqs":
        return pow(np.sin(x), 0.5)
    elif func == "l":
        return np.log(x)

def min_val(a, b, func, A, n):
    partitions = 10000
    min = 100000000000000000000000000000000000000
    for i in range(partitions):
        val = f(a + (b - a) / partitions * (i - 1), func, A, n)
        if val < min:
            min = val

    if (min > 0):
        min = 0

    return min * 1.05


def max_val(a, b, func, A, n):
    partitions = 10000
    max = -100000000000000000000000000000000000000
    for i in range(partitions):
        val = f(a + (b - a) / partitions * (i - 1), func, A, n)
        if val > max:
            max = val

    return max * 1.05


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_f()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
