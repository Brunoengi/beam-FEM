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
    - No unit conversion is performed internally.
    - The element formulation assumes **Euler–Bernoulli beam theory**.
    """

    def __init__(self, I, E, A, start, end):
        
        self.I = I
        self.E = E
        self.A = A
        self.start = start
        self.end = end