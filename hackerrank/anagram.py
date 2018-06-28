from collections import Counter

lines = int(input())
for _ in range(lines):
    s1s2 = input()
    if len(s1s2) % 2 == 1:
        print(-1)
    else:
        s1 = Counter(s1s2[:int(len(s1s2) / 2)])
        s2 = Counter(s1s2[int(len(s1s2) / 2):])
        s1.subtract(s2)
        print(sum(abs(i) for i in s1.values()) // 2)
