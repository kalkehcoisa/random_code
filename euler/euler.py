import math

def is_prime(number):
    if number == 2:
        return True
    elif number < 2:
        return False
    max = math.sqrt(number)
    number_aux = number
    for p in range(2, int(max)+1 ):
        while( number_aux % p == 0 ):
            number_aux = number_aux / p
            return False
    return True

def num_divisors(number):
    max = int( math.sqrt(number) )+1
    cont = 1
    p = 1
    while(p < max):
        if( number % p == 0 ):
            cont += 2
        p += 1
    return cont

def divisors(number):
    max = int(math.sqrt(number))+1
    list = [1]
    p = 2
    while(p < max):
        if( number % p == 0 ):
            list.extend([p, number/p])
        p += 1
    list.append(number)
    return list


def sum_divisors(number):
    max = int(math.sqrt(number))+1
    sum = 1
    p = 2
    while(p < max):
        if( number % p == 0 ):
            sum += (p + number/p)
        p += 1
    return sum



def is_rational(number):
    try:
        return float(int( math.sqrt(number) )) < math.sqrt(number)
    except:
        return False

def is_permutation(number, number2):
    if number == number2:
        return False
    number = str(number)
    number2 = str(number2)
    for c in number:
        test = False
        for p in number2:
            if c == p:
                test = True
                number2 = number2.replace(c, 'a', 1)
                break
        if not test:
            return False
    return True

def prime_factors(number):
    max = math.sqrt(number)
    number_aux = number
    factor = 0
    prime_list = {}
    for p in range(2, int(math.ceil(max))+1 ):
        counter = 0
        while( number_aux % p == 0 ):
            number_aux = number_aux / p
            factor = p
            counter = counter + 1
        if factor == p:
            prime_list[str(p)] = counter
    return prime_list

def max_prime_factor(number):
    max = math.sqrt(number)
    number_aux = number

    for p in range(2, int(math.ceil(max)) ):
        while( number_aux % p == 0 ):
            number_aux = number_aux / p
            factor = p
    return factor