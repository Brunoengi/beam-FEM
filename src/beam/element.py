import math
import sympy as sp
from .node import Node


class Element:
    """
    2D Euler–Bernoulli beam element with 6 DOFs (ux, uy, rz at each node).

    Units (must be consistent):
    ---------------------------
    Length  : cm
    Area    : cm²
    Inertia : cm⁴
    Force   : kN
    Moment  : kN·cm
    """

    def __init__(self, node_i: Node, node_j: Node, E: float, A: float, I: float, q: float = 0.0):
        sp.init_printing()

        self.node_i = node_i
        self.node_j = node_j

        self.E = E
        self.A = A
        self.I = I
        self.q = q


        # ------------------------------------------------------------------
        # Geometry
        # ------------------------------------------------------------------
        self.L = self._length()
        self.theta = self._angle()

        # ------------------------------------------------------------------
        # Global DOFs (connectivity)
        # ------------------------------------------------------------------
        self.dofs = (
            *self.node_i.dofs,
            *self.node_j.dofs
        )

        # ------------------------------------------------------------------
        # Symbolic formulation
        # ------------------------------------------------------------------
        E_s, A_s, I_s, L_s, theta_s, c, s = self.create_symbols()

        ke_local = self.symbolic_ke_(E_s, A_s, I_s, L_s)
        T = self.T(c, s)
        ke_global_symbolic = self.symbolic_ke(T, ke_local)

        self.ke_global = self.calculate_ke(
            ke_global_symbolic,
            E_s, A_s, I_s, L_s, theta_s
        )


    def equivalent_nodal_load_local(self) -> sp.Matrix:
        """
        Equivalent nodal load vector for a uniformly distributed load q.
        Local coordinates.
        """
        q = self.q
        L = self.L

        return sp.Matrix([
            0,
            q * L / 2,
            q * L**2 / 12,
            0,
            q * L / 2,
            -q * L**2 / 12
        ])

    def equivalent_nodal_load_global(self) -> sp.Matrix:
        """
        Transform equivalent nodal loads to global coordinates.
        """
        I_s, E_s, A_s, L_s, theta_s, c, s = self.create_symbols()
        T = self.T(c, s)

        f_local = self.equivalent_nodal_load_local()

        # substitui c e s pelos valores reais
        T_num = T.subs({
            c: math.cos(self.theta),
            s: math.sin(self.theta)
        })

        return T_num.T * f_local
    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------

    def _length(self) -> float:
        dx = self.node_j.x - self.node_i.x
        dy = self.node_j.y - self.node_i.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def _angle(self) -> float:
        dx = self.node_j.x - self.node_i.x
        dy = self.node_j.y - self.node_i.y
        return math.atan2(dy, dx)

    # ------------------------------------------------------------------
    # Symbolic helpers
    # ------------------------------------------------------------------

    def create_symbols(self):
        """
        Create symbolic variables for stiffness derivation.
        """
        E, A, I, L, theta = sp.symbols("E A I L theta")
        c = sp.cos(theta)
        s = sp.sin(theta)
        return E, A, I, L, theta, c, s

    def symbolic_ke_(self, E, A, I, L):
        """
        Local stiffness matrix (Euler–Bernoulli beam).
        """
        return sp.Matrix([
            [ E*A/L,            0,              0, -E*A/L,            0,              0],
            [     0,  12*E*I/L**3,  6*E*I/L**2,       0, -12*E*I/L**3,  6*E*I/L**2],
            [     0,   6*E*I/L**2,    4*E*I/L,       0,  -6*E*I/L**2,    2*E*I/L],
            [-E*A/L,            0,              0,  E*A/L,            0,              0],
            [     0, -12*E*I/L**3, -6*E*I/L**2,       0,  12*E*I/L**3, -6*E*I/L**2],
            [     0,   6*E*I/L**2,    2*E*I/L,       0,  -6*E*I/L**2,    4*E*I/L],
        ])

    def T(self, c, s):
        """
        Transformation matrix (local → global).
        """
        return sp.Matrix([
            [ c, -s, 0,  0,  0, 0],
            [ s,  c, 0,  0,  0, 0],
            [ 0,  0, 1,  0,  0, 0],
            [ 0,  0, 0,  c, -s, 0],
            [ 0,  0, 0,  s,  c, 0],
            [ 0,  0, 0,  0,  0, 1],
        ])

    def symbolic_ke(self, T, ke_local):
        """
        Global stiffness matrix (symbolic).
        """
        return T.T * ke_local * T

    def calculate_ke(self, ke, E, A, I, L, theta):
        """
        Substitute numerical values into symbolic stiffness matrix.
        """
        return ke.subs({
            E: self.E,
            A: self.A,
            I: self.I,
            L: self.L,
            theta: self.theta
        })