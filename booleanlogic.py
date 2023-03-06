# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def check_prior(a):
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        return 2

# и для дистанции на каждом
def check_dist(a):
    if a < 30:
        return 0
    if (a > 30) and (a < 70):
        return 1
    if a > 70:
        return 2


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    target_sector = 1
    mid = 20
    left = 40
    right = 100
    indl = check_dist(left)
    indm = check_dist(mid)
    indr = check_dist(right)
    indp = check_prior(target_sector)
    print(indl, indm, indr, indp)
    solution_num= indp+3*indr+9*indm+27*indm
    print("Ситуация номер ",solution_num)
    # и достаем из массива решение по номеру


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
