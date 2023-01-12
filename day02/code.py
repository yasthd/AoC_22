# Rock: 0, Paper: 1, Scissor: 2

conversion = {"A":0, "B":1, "C":2, "X":0, "Y":1, "Z":2}

def score(a:int, b:int) -> int:
    if a == b:
        return b+1+3
    elif ((a+1) % 3) == b:
        return b+1+6
    else:
        return b+1

def score2(a:int, b:int) -> int:
    if b == 0:
        return ((a-1) % 3)+1
    if b == 1:
        return a+1+3
    if b == 2:
        return ((a+1) % 3)+1+6

def parse(guide:str) -> list[tuple[int]]:
    return [tuple(map(lambda x: conversion[x], line.split())) for line in guide.strip().split("\n")]

with open("input") as f:
    parsed = parse(f.read())
    print(sum(score2(a, b) for a, b in parsed))
