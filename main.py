import numpy as np  # used to generate the random x and y coordinates, as well as calculating the standard deviation and mean from a list
import math  # used to calculate a square root
import time  # used to take the runtime
import threading  # used to implement parallelization
from queue import Queue  # used to store the results from each thread


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

    p_tot = 1000

    min = min_val(a, b, func, A, n)
    max = max_val(a, b, func, A, n)

    # print(min, max)

    start = time.time()  # start a chronometer to see how much time the simulation takes

    res = []  # list to store all the results

    num_threads = 10
    cycles_per_thread = N / num_threads
    threads = []
    queue = Queue()

    for t in range(num_threads):
        # Create and start the thread
        thread = threading.Thread(target=worker, args=(queue, t, a, b, min, max, cycles_per_thread, func, A, n, p_tot))
        thread.start()

        # Add the thread to the list
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
        res.extend(queue.get())

    stdev = np.std(res,
                   ddof=1)  # calculate the standard deviation; important note: the 'ddof=1' parameter is used so that the standard deviation of a SAMPLE is calculated (i.e., the division of the differences of each value from the mean is divided by N-1), otherwise, the STDEV of the populations is calculated (i.e., the division of the differences of each value from the mean is divided by N).
    se = stdev / math.sqrt(N)  # calculate the standard error of the mean value
    mean = np.mean(res)  # calculate the mean
    end = time.time()  # save the endtime

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

    tex_res = open("tex-res.txt", "a+")
    # FORMAT mean stdev se N p_tot t num_desc a b
    tex_res.write(
        f'{mean} {stdev} {se} {N} {p_tot} {end - start} {num_desc(func)} {a} {b}\n'
    )  # Write results to res.txt file
    tex_res.close()


def worker(queue, t, a, b, min, max, N, func, A, n, p_tot):
    res = []  # list to store the results of the thread
    print(f"Thread {t} started")

    for i in range(int(N)): # repeat N times (i.e., generate n πs)
        p_in = 0  # variable that stores the points that were within the circle

        for m in range(p_tot):  # repeat for p_tot points (i.e., generate p_tot points)
            x = np.random.uniform(a, b)  # generate x coordinate
            y = np.random.uniform(min, max)  # generate y coordinate

            f_x = f(x, func, A, n)
            # print(x, f_x)
            # print(x, y)

            if y > 0 and y <= f_x:
                p_in += 1
            elif y < 0 and y <= f_x:
                p_in -= 1

        # print(f"ratio: {(p_pos - p_neg)/p_tot}")

        area = (b - a) * (max - min) * (p_in / p_tot)

        res.append(area)

    print(f"Thread {t} FINISHED")
    queue.put(res)


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
