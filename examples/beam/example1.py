from beam import Element, System



beam1 = Element(1, 1, 1, 0, 1, 1, 2, 3, 4, 5, 6, 0)
beam2 = Element(1, 1, 1, 0, 1, 1, 2, 3, 7, 8, 9, 0)
system = System([beam1, beam2])
print(system.ke)