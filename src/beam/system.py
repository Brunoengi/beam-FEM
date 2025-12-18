from typing import List
from .element import Element
import sympy as sp

class System:
    def __init__(self, elements: List[Element]):
        self.elements = elements
        self.ke = self.calculate_ke(elements)
        
        S1, S2, S3, S4, S5, S6, S7, S8, S9, q1, q2, q3, q4, q5, q6, q7, q8, q9 = self.create_symbols()
        F = sp.Matrix([S1, S2, 0, 0, -100e3, 0, S7, S8, 0])
        u = sp.Matrix([0, 0, q3, q4, q5, q6, 0, 0, q9])
        
        system = self.ke * u - F
        result = sp.linsolve(system, (S1, S2, q3, q4, q5, q6, S7, S8, q9))
        print(result)

    
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

    def create_symbols(self):
        ##Esforços
        symbols_force = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
        
        ##Displace
        symbols_displace = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9']
        
        S1, S2, S3, S4, S5, S6, S7, S8, S9 = sp.symbols(symbols_force)
        q1, q2, q3, q4, q5, q6, q7, q8, q9 = sp.symbols(symbols_displace)
        
        return S1, S2, S3, S4, S5, S6, S7, S8, S9, q1, q2, q3, q4, q5, q6, q7, q8, q9

        
        