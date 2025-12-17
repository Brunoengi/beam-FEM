import sympy as sp

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

    Notes
    -----
    - All input values **must strictly follow** the unit system:
        Length → cm  
        Area → cm²  
        Second moment of area → cm⁴  
        Stress / modulus → kN/cm²
    """

    def __init__(self):
        
        sp.init_printing()
        
        # self.I = I
        # self.E = E
        # self.A = A
        # self.start = start
        # self.end = end
        # self.L = end - start
        
        I, E, A, L, theta, c, s = self.create_symbols()
        ke_ = self.ke_(E, A, I, L)
        T = self.T(c,s)
        self.Ke = self.Ke(T, ke_)
        print(self.Ke)
        
    def create_symbols(self):
        I, E, L, A, theta = sp.symbols(['I', 'E', 'L', 'A', 'theta'])
        c = sp.cos(theta)
        s = sp.sin(theta)
        return I, E, L, A, theta, c, s
  
    def ke_(self, E, A, I, L):
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
    
    def T(self, c,s):
        T = sp.Matrix([
            [c, -s, 0, 0, 0, 0],
            [s, c, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, c, -s, 0],
            [0, 0, 0, s, c, 0],
            [0, 0, 0, 0, 0, 1]  
        ])
        return T
    
    def Ke(self, T, ke_):
        return T.T * ke_ * T
    

ele = Element()