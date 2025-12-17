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

    def __init__(self, I_, E_, A_, start, end, theta_=0.0):
        
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
        
        
        ke_global = self.calculate_ke(symbolic_ke_global, I_, A_, E_, self.L, theta_, I, E, A, L, theta)
        print(ke_global)
        
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
    
    def calculate_ke(self, ke, I_, A_, E_, L_, theta_, I, E, A, L, theta):
        """
        Replace symbolic values ​​with numerical values
        """
        theta_ = theta_ *math.pi /180.
        k_element = ke.subs({I: I_, A: A_, E: E_, L: L_, theta: theta_})
        return k_element
    
    
el = Element(300, 70e3, 40., 0, 200, 30)

