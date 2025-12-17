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

    def __init__(self, I, E, A, start, end):
        
        self.I = I
        self.E = E
        self.A = A
        self.start = start
        self.end = end
        self.L = end - start
        
        def create_symbols():
            I, E, L, A, theta = sp.symbols('I', 'E', 'L', 'A', 'theta')
            return I, E, L, A, theta
        
        def ke_(E, A, I, L):
            sp.Matrix([
                [E * A / L, 0, 0, -E*A/L, 0, 0],
                [0, 12 *E * I / L ** 3, 6 * E * I / L ** 2, 0, -12 * E * I / L ** 3, 6 * E * I / L ** 2],
                [0, 6 * E * I / L ** 2, 4 * E * I / L, 0, -6 * E * I / L ** 2, 2 * E * I / L],
                [-E * A / L, 0, 0, E * A / L, 0, 0],
                [0, -12 * E * I / L ** 3, -6 * E * I / L ** 2, 0, 12 * E * I / L ** 3, -6 * E * I / L ** 2],
                [0, 6 * E * I / L ** 2, 2 * E * I / L, 0, -6 * E * I / L ** 2, 4 * E * I / L]
            ])