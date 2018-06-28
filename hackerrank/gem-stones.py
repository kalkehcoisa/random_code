lines = int(input())
gems = set(chr(i) for i in range(ord('a'), ord('z') + 1))
for _ in range(lines):
    gems = gems & set(input())
print(len(gems))
