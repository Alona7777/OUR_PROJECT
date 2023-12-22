def rec(numbers):
    result = numbers
    count = 1
    if numbers <= 1:
        return result
    else:
        result += rec(numbers - 1)
    return result


print(rec(10))


def recurs(num):

    if not num:
        return 0
    else:
        return num + recurs(num - 1)
    

print(recurs(10))