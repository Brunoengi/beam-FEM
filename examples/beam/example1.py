from beam import Element, System

beam1 = Element(40*80**3/12, 70000, 40*80, 0, 3* 1000/4, 1, 2, 3, 4, 5, 6, 0)
beam2 = Element(40*80**3/12, 70000, 40*80, 0, 1* 1000/4, 4, 5, 6, 7, 8, 9, 0)
system = System([beam1, beam2])
print(system.ke)