import sympy as sp
import math

class Element:
    """
    Beam element for structural analysis using the Finite Element Method (FEM).

    This class represents a 1D Euler–Bernoulli beam element with constant
    mechanical and geometric properties.

    Parameters
    ----------
    I : float
        Second moment of area  
        Unit: cm⁴
    E : float
        Young's modulus  
        Unit: kN/cm²
    A : float
        Cross-sectional area  
        Unit: cm²
    start : float
        Initial coordinate of the element along the local x-axis  
        Unit: cm
    end : float
        Final coordinate of the element along the local x-axis  
        Unit: cm
    theta: float
        Unit: Graus

    Notes
    -----
    - All input values **must strictly follow** the unit system:
        Length → cm  
        Area → cm²  
        Second moment of area → cm⁴  
        Stress / modulus → kN/cm²
    """

    def __init__(self, I_, E_, A_, start, end, g1, g2, g3, g4, g5, g6, theta_=0.0):
        
        sp.init_printing()
        
        self.I = I_
        self.E = E_
        self.A = A_
        self.start = start
        self.end = end
        self.L = end - start
        
        ##Defined in terms of symbolic variables
        I, E, A, L, theta, c, s = self.create_symbols()
   
        symbolic_ke_local = self.symbolic_ke_(E, A, I, L)
        T = self.T(c, s)
        symbolic_ke_global = self.symbolic_ke(T, symbolic_ke_local)
        
        self.ke_global = self.calculate_ke(symbolic_ke_global, I_, A_, E_, self.L, theta_, I, E, A, L, theta, g1, g2, g3, g4, g5, g6)
        
        
    def create_symbols(self):
        I, E, L, A, theta = sp.symbols(['I', 'E', 'L', 'A', 'theta'])
        c = sp.cos(theta)
        s = sp.sin(theta)
        
    
        
        return I, E, L, A, theta, c, s
  
    def symbolic_ke_(self, E, A, I, L):
        """
        Computes the local stiffness matrix of a beam element
        based on Euler–Bernoulli beam theory. The element has 6 degrees of freedom.

        Parameters
        ----------
        E : float
            Young's modulus of the material.
        A : float
            Cross-sectional area.
        I : float
            Second moment of area.
        L : float
            Element length.

        Returns
        -------
        ke : sympy.Matrix
            Local stiffness matrix (6x6) in the element coordinate system.
        """
        ke_ = sp.Matrix([
            [E * A / L, 0, 0, -E*A/L, 0, 0],
            [0, 12 *E * I / L ** 3, 6 * E * I / L ** 2, 0, -12 * E * I / L ** 3, 6 * E * I / L ** 2],
            [0, 6 * E * I / L ** 2, 4 * E * I / L, 0, -6 * E * I / L ** 2, 2 * E * I / L],
            [-E * A / L, 0, 0, E * A / L, 0, 0],
            [0, -12 * E * I / L ** 3, -6 * E * I / L ** 2, 0, 12 * E * I / L ** 3, -6 * E * I / L ** 2],
            [0, 6 * E * I / L ** 2, 2 * E * I / L, 0, -6 * E * I / L ** 2, 4 * E * I / L]
        ])
        return ke_
    
    def T(self, c, s):
        T = sp.Matrix([
            [c, -s, 0, 0, 0, 0],
            [s, c, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, c, -s, 0],
            [0, 0, 0, s, c, 0],
            [0, 0, 0, 0, 0, 1]  
        ]).T
        return T
    
    def symbolic_ke(self, T, ke_):
        return T.T * ke_ * T
    
    def calculate_ke(self, ke, I_, A_, E_, L_, theta_, I, E, A, L, theta, g1, g2, g3, g4, g5, g6):
        """
        Replace symbolic values ​​with numerical values
        """
        theta_ = theta_ *math.pi /180.
        k_element = ke.subs({I: I_, A: A_, E: E_, L: L_, theta: theta_})
        
        k_element = k_element.row_insert(0, sp.Matrix([[g1, g2, g3, g4, g5, g6]]))
        k_element = k_element.col_insert(0, sp.Matrix([0, g1, g2, g3, g4, g5, g6]))
        
        return k_element
    
    def force(S1, S2, S3, S4, S5, S6, S7, S8, S9):
        F = sp.Matrix([S1, S2, 0, 0, -110e3, 0, S7, S8, 0])
        return F

    def displace(q1, q2, q3, q4, q5, q6, q7, q8, q9):
        u = sp.Matrix([0, 0, q3, q4, q5, q6, 0, 0, q9])  
        return u

