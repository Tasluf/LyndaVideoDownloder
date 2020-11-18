import timeit


def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        total_time = sum(runs) / len(runs)
        if total_time >= 60:
            total_time = total_time / 60
            print(f"Total time: {total_time} Minute")
        else:
            print(f"Total time: {total_time} second")

    return wrapper
