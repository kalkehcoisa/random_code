def palidrome_index(word):
    if len(word) == 1:
        return -1

    ini = word[0:len(word) // 2]
    end = word[len(word) // 2 + len(word) % 2::][::-1]

    if ini.startswith(end):
        return -1
    else:
        checks = (ini[i] != end[i] for i in range(len(ini)))
        for i, v in enumerate(checks):
            if v:
                return i
        else:
            return -1


print(palidrome_index('abccbx'))
print(palidrome_index('aaaaaa'))
print(palidrome_index('bbb'))
print(palidrome_index('quack'))
