import numpy as np  # used to generate the random x and y coordinates, as well as calculating the standard deviation and mean from a list
import math  # used to calculate a square root
import time  # used to take the runtime
import multiprocessing  # used to run multiple processes (parallelization)
from multiprocessing import Pool  # used to create a pool of workers for parallelization


# function to generate a string description of the function
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


# function to get the numerical index of a function
def num_desc(func):
    if func == "n":
        return 1
    elif func == "p":
        return 2
    elif func == "s":
        return 3
    elif func == "c":
        return 4
    elif func == "sqs":
        return 5
    elif func == "l":
        return 6


# function to print all the options in array; one per line
def print_arr(arr):
    res = ""
    for el in arr:
        res += el + "\n"

    return res


# main function
def main_f():
    auto_in = input(f"Would you like to perform the autorun routine (pre-programmed values)? (y/n) ").strip()  # chose if the autorun routine will be performed
    if auto_in == "y":
        auto()
    elif auto_in == "n":
        manual()


def auto():
    # These routines were performed to generate the values for the report
    # fs = ("n: e^(-x^2)", "p: Ax^n", "s: sin(x)", "sqs: sqrt(sin(x))", "c: cos(x)", "l: ln(x)")
    #integrate("p", 10, -3, 3, 1000, 1, 2)
    #integrate("p", 100, -3, 3, 1000, 1, 2)
    #integrate("p", 1000, -3, 3, 1000, 1, 2)
    #integrate("p", 10000, -3, 3, 1000, 1, 2)
    #integrate("s", 10000, 0, 3.141592653589793, 1000, 1, 2)
    #integrate("p", 100000, -3, 3, 1000, 1, 2)
    integrate("p", 10, 3, 6, 1000, 1, 2)
    integrate("p", 30, 3, 6, 1000, 1, 2)
    integrate("p", 100, 3, 6, 1000, 1, 2)
    integrate("p", 300, 3, 6, 1000, 1, 2)
    integrate("p", 1000, 3, 6, 1000, 1, 2)
    integrate("p", 3000, 3, 6, 1000, 1, 2)
    integrate("p", 10000, 3, 6, 1000, 1, 2)
    integrate("p", 30000, 3, 6, 1000, 1, 2)
    integrate("p", 100000, 3, 6, 1000, 1, 2)


def manual():
    fs = ("n: e^(-x^2)", "p: Ax^n", "s: sin(x)", "sqs: sqrt(sin(x))", "c: cos(x)", "l: ln(x)")
    func = input(f"Select a function to integrate:\n{print_arr(fs)} ").strip()  # select function to be integrated

    print(f"The function to integrate is {desc(func)}")  # output function to be integrated

    if func == "p":  # if the chose function is a polynomial, as for the A and n parameters (for Ax^n)
        A = float(input(f"Input the value of A: "))
        n = float(input(f"Input the value of n: "))
    else:  # otherwise, set A and n to 0, as they are irrelevant parameters
        A = 0
        n = 0

    N = int(input("Enter the value of N (number of repetitions): "))  # ask for N

    a = float(input("Enter the value of a: ")) # ask for a
    b = float(input("Enter the value of b: ")) # ask for b

    p_tot = 1000  # set p_tot

    integrate(func, N, a, b, p_tot, A, n)  # integrate with the given parameter


# integrate function
def integrate(func, N, a, b, p_tot, A, n):
    min = min_val(a, b, func, A, n)  # calculate the min value for a <= x <= b
    max = max_val(a, b, func, A, n)  # calculate the max value for a <= x <= b

    start = time.time()  # start a chronometer to see how much time the simulation takes

    res = []  # list to store all the results

    num_threads = 10  # total number of threads
    pool = Pool(processes=num_threads)  # generate a pool with the number of processes = number of desired threads
    results_pool = pool.apply_async(worker, (a, b, min, max, N, func, A, n, p_tot))  # use the pool to do the `worker` function with the parameters of the integral to be calculated
    res.extend(results_pool.get())  # add the results of the pool to the res list

    stdev = np.std(res,
                   ddof=1)  # calculate the standard deviation; important note: the 'ddof=1' parameter is used so that the standard deviation of a SAMPLE is calculated (i.e., the division of the differences of each value from the mean is divided by N-1), otherwise, the STDEV of the populations is calculated (i.e., the division of the differences of each value from the mean is divided by N).
    se = stdev / math.sqrt(N)  # calculate the standard error of the mean value
    mean = np.mean(res)  # calculate the mean
    end = time.time()  # save the endtime

    # additional A and n parameter for the polynomial function
    additional = ""
    if func == "p":
        additional = f", A: {A}, n: {n}"

    print(
        f'Mean: {mean}, Std. Dev.: {stdev}, Std. Err.: {se}, n: {N}, pTot: {p_tot}, t: {end - start}, f: {desc(func)}, a: {a}, b: {b}{additional}\n'
    )  # print the results

    results = open("res.txt", "a+")
    results.write(
        f'Mean: {mean}, Std. Dev.: {stdev}, Std. Err.: {se}, n: {N}, pTot: {p_tot}, t: {end - start}, f: {desc(func)}, a: {a}, b: {b}{additional}\n'
    )  # Write results to res.txt file
    results.close()

    # results in LaTeX format for gnuplot
    tex_res = open("tex-res.txt", "a+")
    # FORMAT mean stdev se N p_tot t num_desc a b
    tex_res.write(
        f'{mean} {stdev} {se} {N} {p_tot} {end - start} {num_desc(func)} {a} {b}\n'
    )  # Write results to res.txt file
    tex_res.close()


# worker function; performs the actual integration
def worker(a, b, min, max, N, func, A, n, p_tot):
    res = []  # list to store the results of the thread

    for i in range(int(N)): # repeat N times (i.e., generate N values)
        p_in = 0  # variable that stores the points that were within the circle

        for m in range(p_tot):  # repeat for p_tot points (i.e., generate p_tot points)
            x = np.random.uniform(a, b)  # generate x coordinate
            y = np.random.uniform(min, max)  # generate y coordinate

            f_x = f(x, func, A, n)  # calculate f(x)

            # compute the in(x_rand, y_rand) function [Equation 3 in the report] for the randomly generated point
            if 0 < y <= f_x:  # test if the point is within the function; above the x-axis
                p_in += 1  # if so, add 1 to the counter of the points within the function
            elif 0 > y >= f_x:  # test if the point is within the function; below the x-axis
                p_in -= 1  # if so, subtract 1 to the counter of the points within the function

        area = (b - a) * (max - min) * (p_in / p_tot)  # calculate the results of the definite integral

        res.append(area)  # append result to the results list

    return res  # return the results list


# calculate f(x) for any given function
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


# calculate the min of f for a <= x <= b with sampling
def min_val(a, b, func, A, n):
    partitions = 10000  # number of samples
    min = 100000000000000000000000000000000000000  # starting min value; as it is replaced, it needs to be very high so that any other value is smaller than the starting value
    for i in range(partitions):  # for each partition
        val = f(a + (b - a) / partitions * (i - 1), func, A, n)  # // sample for x = a + delta_x * (i - 1); with this, the sampling starts at a and finishes at b, adding delta_x for each iteration
        if val < min:  # if the current sample is smaller than the previous maximum value, replace it
            min = val

    if min > 0:  # if min > 0, min = 0 (because the integral should always be at least from the x-axis or below
        min = 0

    return min * 1.05  # multiply the min by 1.05 to account for some possible missed values in the sampling (so that the value is smaller, i.e. y is 'lower', therefore a greater area is covered)


# calculate the max of f for a <= x <= b with sampling
def max_val(a, b, func, A, n):
    partitions = 10000  # number of samples
    max = -100000000000000000000000000000000000000  # starting max value; as it is replaced, it needs to be very low so that any other value is greater than the starting value
    for i in range(partitions):  # for each partition
        val = f(a + (b - a) / partitions * (i - 1), func, A, n)   # // sample for x = a + delta_x * (i - 1); with this, the sampling starts at a and finishes at b, adding delta_x for each iteration
        if val > max:  # if the current sample is greater than the previous maximum value, replace it
            max = val

    return max * 1.05  # multiply the min by 1.05 to account for some possible missed values in the sampling (so that the value is larger, i.e. y is 'above', therefore a greater area is covered)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_f()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
