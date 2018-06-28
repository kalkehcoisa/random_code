lines = int(input())
for _ in range(2 * lines):
    w1 = set(input())
    w2 = set(input())
    if len(w1 & w2):
        print('YES')
    else:
        print('NO')
