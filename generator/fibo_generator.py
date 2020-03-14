def fibo_gen(n):
    numbers = []
    for i in range(n):
        if i == 0:
            numbers.append(0)
            yield 0
        elif i == 1:
            numbers.append(1)
            yield 1
        else:
            result = numbers[i - 1] + numbers[i - 2]
            numbers.append(result)
            yield result
