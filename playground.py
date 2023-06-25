import concurrent.futures
from time import sleep


def func1(p):
    while True:
        print(f"F1: {p}")
        sleep(2)


def func2(p):
    while True:
        print(f"F2: {p}")
        sleep(6)


calls = []

num = 1
while num != 0:
    num = int(input("1 or 2: "))
    name = input("Name: ")

    if num == 1:
        calls.append((func1, name))
    elif num == 2:
        calls.append((func2, name))

    print()

with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as executor:
    for call in calls:
        executor.map(call[0], (call[1],))
