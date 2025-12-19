from typing import List
import sympy as sp

from .element import Element
from .node import Node


class System:
    """
    Structural system assembled using the Finite Element Method (FEM).
    """

    def __init__(self, elements: List[Element]):
        self.elements = elements
        self.nodes = self._collect_nodes(elements)

        self.ndof = self._total_dofs()

        self.K = self.assemble_stiffness()
        self.F = self.assemble_force_vector()

        # Prescribed displacements (dict: dof -> value)
        self.prescribed_dofs = self.assemble_prescribed_dofs()

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _collect_nodes(self, elements: List[Element]) -> List[Node]:
        nodes: List[Node] = []

        for el in elements:
            if el.node_i not in nodes:
                nodes.append(el.node_i)
            if el.node_j not in nodes:
                nodes.append(el.node_j)

        return nodes

    def _total_dofs(self) -> int:
        return max(dof for node in self.nodes for dof in node.dofs)

    # ------------------------------------------------------------------
    # Assembly
    # ------------------------------------------------------------------

    def assemble_stiffness(self) -> sp.Matrix:
        K = sp.Matrix.zeros(self.ndof, self.ndof)

        for el in self.elements:
            ke = el.ke_global
            dofs = [d - 1 for d in el.dofs]

            for i in range(6):
                for j in range(6):
                    K[dofs[i], dofs[j]] += ke[i, j]

        return K

    def assemble_force_vector(self) -> sp.Matrix:
        F = sp.Matrix.zeros(self.ndof, 1)

        for node in self.nodes:
            fx = node.actions.get("fx", 0)
            fy = node.actions.get("fy", 0)
            mz = node.actions.get("mz", 0)

            dofs = [d - 1 for d in node.dofs]

            F[dofs[0]] += fx
            F[dofs[1]] += fy
            F[dofs[2]] += mz

        return F

    def assemble_prescribed_dofs(self):
        """
        Returns:
            dict { global_dof_index (0-based) : prescribed displacement }
        """
        prescribed = {}

        for node in self.nodes:
            dofs = [d - 1 for d in node.dofs]

            if node.displacements.get("ux") is not None:
                prescribed[dofs[0]] = node.displacements["ux"]

            if node.displacements.get("uy") is not None:
                prescribed[dofs[1]] = node.displacements["uy"]

            if node.displacements.get("rz") is not None:
                prescribed[dofs[2]] = node.displacements["rz"]

        return prescribed

    # ------------------------------------------------------------------
    # Solution
    # ------------------------------------------------------------------

    def partition_dofs(self):
        fixed = sorted(self.prescribed_dofs.keys())
        free = [i for i in range(self.ndof) if i not in fixed]
        return free, fixed

    def solve(self):
        free, fixed = self.partition_dofs()

        K_ff = self.K.extract(free, free)
        K_fc = self.K.extract(free, fixed)
        K_cf = self.K.extract(fixed, free)
        K_cc = self.K.extract(fixed, fixed)

        F_f = self.F.extract(free, [0])
        F_c = self.F.extract(fixed, [0])

        u_c = sp.Matrix([self.prescribed_dofs[d] for d in fixed])

        # Solve free displacements
        u_f = K_ff.LUsolve(F_f - K_fc * u_c)

        # Reactions
        #Vetor global de reações
        R = sp.Matrix.zeros(self.ndof, 1)

        # Calcula reações apenas nos DOFs fixos
        R_c = K_cf * u_f + K_cc * u_c - F_c

        for i, dof in enumerate(fixed):
            R[dof] = R_c[i]

        # Full displacement vector
        u = sp.Matrix.zeros(self.ndof, 1)

        for i, d in enumerate(free):
            u[d] = u_f[i]

        for i, d in enumerate(fixed):
            u[d] = u_c[i]

        return u, R