#Input a list of demical values <1
#Returns the best partition of two balanced lists

def computeBestPartition(l):
    n = len(l)
    assert n >= 1
    assert all(elt >= 1 and elt == int(elt) for elt in l)
    # your code here

    sorted_l = sorted(l, reverse=True)

    l1 = []
    l2 = []

    left = True

    for num in sorted_l:
        if left == True:
            l1.append(num)
            left = False
        else:
            l2.append(num)
            left = True

    list_diff = (abs(sum(l1) - sum(l2)))

    while list_diff > 1:

        mid_diff = list_diff / 2

        print(f"initial difference is {list_diff}")

        closest_number_l1 = min(l1, key=lambda x: abs(x - mid_diff))
        closest_number_l2 = min(l2, key=lambda x: abs(x - mid_diff))

        if sum(l1) > sum(l2):
            l1.remove(closest_number_l1)
            l2.append(closest_number_l1)
            print(f"donating {closest_number_l1} to l2")

        else:
            l2.remove(closest_number_l2)
            l1.append(closest_number_l2)
            print(f"donating {closest_number_l2} to l1")

        list_diff = (abs(sum(l1) - sum(l2)))

        print(f"new difference is {list_diff}")


    return(l1,l2)
