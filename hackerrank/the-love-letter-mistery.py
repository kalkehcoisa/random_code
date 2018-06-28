lines = int(input())
for _ in range(lines):
    str1 = input()
    extra = len(str1) % 2
    ini = str1[:int(len(str1) / 2)]
    end = str1[int(len(str1) / 2) + extra:][::-1]
    soma = sum(abs(ord(i) - ord(j)) for i, j in zip(ini, end))
    print(soma)
