from beam import Node, Element, System

node_1 = Node(
    position={"x": 0.0, "y": 0.0},
    label="N1",
    actions={"fx": 0.0, "fy": 0.0, "mz": 0.0},
    displacements={
        "ux": 0.0, 
        "uy": 0.0,
        "rz": None
    }
)

node_2 = Node(
    position={"x": 750.0, "y": 0.0},
    label="N2",
    actions={"fx": 0.0, "fy": -100.0, "mz": 0.0},  # carga pontual
    displacements={"ux": None, "uy": None, "rz": None}
)

node_3 = Node(
    position={"x": 1000.0, "y": 0.0},
    label="N3",
    actions={"fx": 0.0, "fy": 0.0, "mz": 0.0},
    displacements={"ux": None, "uy": 0.0, "rz": None}  # apoio simples
)

# --------------------------------------------------
# PROPRIEDADES
# --------------------------------------------------

E = 21000.0     # kN/cm²
A = 100.0       # cm²
I = 8000.0      # cm⁴

# --------------------------------------------------
# ELEMENTOS
# --------------------------------------------------

element_1 = Element(node_1, node_2, E, A, I)
element_2 = Element(node_2, node_3, E, A, I)

# --------------------------------------------------
# SISTEMA
# --------------------------------------------------

system = System([element_1, element_2])

u, reactions = system.solve()

print("Deslocamentos globais:")
print(u)

print("\nReações globais:")
print(reactions)