from collections import Counter
str1, str2 = Counter(input()), Counter(input())
str1.subtract(str2)
print(sum(abs(i) for i in str1.values()))
