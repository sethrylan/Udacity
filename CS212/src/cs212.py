
def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    result, maxval = [], None
    k = key or (lambda x: x)

    for x in iterable:
        xval = k(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append[x]

    return result


if __name__ == "__main__":
    allmax([1,1])
    print "Hello World";