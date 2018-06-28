from euler import *


def problem_67():
    from numpy import array
    f = open("067.txt", "r").readlines()
    data = []
    for line in f:
        temp = []
        for token in line.replace("\n", "").split(' '):
            temp.append( int(token) )
        data.append(temp)

    leng = len(data)
    while leng-2 >= 0:
        cont = 0
        for p in data[leng-2]:
            if data[leng-1][cont] > data[leng-1][cont+1]:
                data[leng-2][cont] += data[leng-1][cont]
            else:
                data[leng-2][cont] += data[leng-1][cont+1]
            cont += 1
        del data[leng-1]
        leng = len(data)
    print data[0][0]


if __name__ == "__main__":
    problem_67()