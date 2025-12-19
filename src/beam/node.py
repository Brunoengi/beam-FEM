from typing import TypedDict

class Actions(TypedDict):
    fx: float
    fy: float
    mz: float

class Displacements(TypedDict):
    ux: float
    uy: float
    rz: float
    
class Position(TypedDict):
    x: float
    y: float

class Node:
    
    _global_dof_counter: int = 0
    
    def __init__(self, position: Position, label: str, actions: Actions, displacements: Displacements):
        self.x = position['x']
        self.y = position['y']
        self.label = label
        self.actions = actions
        self.displacements = displacements

        # Geração automática dos DOFs do nó
        self.dofs = self._generate_dofs()

    @classmethod
    def _generate_dofs(cls) -> tuple[int, int, int]:
        cls._global_dof_counter += 3
        return (
            cls._global_dof_counter - 2,
            cls._global_dof_counter - 1,
            cls._global_dof_counter
        )

    