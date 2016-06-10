# -*- coding: utf-8 -*-


def DistJaccard(str1, str2):
    str1 = set(str1.lower().split())
    str2 = set(str2.lower().split())
    return float(len(str1 & str2)) / len(str1 | str2)


def levenshtein(s, t):
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)
    v0 = [None] * (len(t.split(" ")) + 1)
    v1 = [None] * (len(t.split(" ")) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s.split(" "))):
        v1[0] = i + 1
        for j in range(len(t.split(" "))):
            cost = 0 if s.split(" ")[i] == t.split(" ")[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t.split(" "))]