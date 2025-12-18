from typing import List
from element import Element
import sympy as sp

class System:
    def __init__(self, elements: List[Element]):
        self.elements = elements
        self.ke = self.calculate_ke(elements)
    
    def calculate_ke(self, elements: list[Element]):
        k_elements = []
        n_elements = len(elements)
        n_GDL = 3 * n_elements + 3
        k_struct = sp.Matrix.zeros(n_GDL, n_GDL)
        
        for i in range(n_elements):
            k_elements.append(elements[i].ke_global)
        
        for n in range(n_elements):
            #Extrai os graus de liberdade do elemento n
            GDL = []
            GDL.append(k_elements[n][0,1] - 1)
            GDL.append(k_elements[n][0,2] - 1)
            GDL.append(k_elements[n][0,3] - 1)
            GDL.append(k_elements[n][0,4] - 1)
            GDL.append(k_elements[n][0,5] - 1)
            GDL.append(k_elements[n][0,6] - 1)
            
            for i in range(len(GDL)):
                for j in range(len(GDL)):
                    k_struct[GDL[i], GDL[j]] += k_elements[n][i+1, j+1]
                    
        return k_struct


        
        
beam1 = Element(1, 1, 1, 0, 1, 1, 2, 3, 4, 5, 6, 0)
beam2 = Element(1, 1, 1, 0, 1, 1, 2, 3, 7, 8, 9, 0)
system = System([beam1, beam2])
print(system.ke)