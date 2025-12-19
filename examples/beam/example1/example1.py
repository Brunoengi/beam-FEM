from beam import Element, System, Node

## Viga Engastada com 10m de comprimento e carga de -10kN na extremidade

## Propriedades Geometricas e dos Materiais
E = 21000.0      # kN/cm² (aço)
A = 100.0        # cm²
I = 8000.0       # cm⁴

node_1 = Node(
    position={"x": 0.0, "y": 0.0},
    label="N1",
    actions={"fx": 0.0, "fy": 0.0, "mz": 0.0},
    displacements={"ux": 0.0, "uy": 0.0, "rz": 0.0}  # engaste
)

node_2 = Node(
    position={"x": 1000.0, "y": 0.0},
    label="N2",
    actions={"fx": 0.0, "fy": -10.0, "mz": 0.0},  # carga pontual
    displacements={"ux": None, "uy": None, "rz": None}  # livre
)

element_1 = Element(
    node_i=node_1,
    node_j=node_2,
    E=E,
    A=A,
    I=I
)

system = System([element_1])

u, reactions = system.solve()
print(u, reactions)