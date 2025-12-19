from beam import Node, Element, System

# ==================================================
# DADOS DO PROBLEMA
# ==================================================

# Comprimento total
L = 1000.0  # cm (10 m)

# Carga distribuída
q = -0.05  # kN/cm  (equivale a -5 kN/m)

# Propriedades do material e seção
E = 21000.0   # kN/cm²
A = 100.0     # cm²
I = 8000.0    # cm⁴

# ==================================================
# NÓS
# ==================================================

# Apoio esquerdo - pino
node_1 = Node(
    position={"x": 0.0, "y": 0.0},
    label="N1",
    actions={"fx": 0.0, "fy": 0.0, "mz": 0.0},
    displacements={
        "ux": 0.0,    # trava X (remove modo rígido)
        "uy": 0.0,    # trava Y
        "rz": None    # rotação livre
    }
)

# Apoio direito - rolete
node_2 = Node(
    position={"x": L, "y": 0.0},
    label="N2",
    actions={"fx": 0.0, "fy": 0.0, "mz": 0.0},
    displacements={
        "ux": None,
        "uy": 0.0,
        "rz": None
    }
)

# ==================================================
# ELEMENTO (com carga distribuída)
# ==================================================

element = Element(
    node_i=node_1,
    node_j=node_2,
    E=E,
    A=A,
    I=I,
    q=q               # <<< carga distribuída uniforme
)

# ==================================================
# SISTEMA
# ==================================================

system = System([element])

u, reactions = system.solve()

# ==================================================
# RESULTADOS
# ==================================================

print("\n================ DESLOCAMENTOS =================")
print("Ordem global dos GDL:")
print("[ux1, uy1, rz1, ux2, uy2, rz2]\n")
print(u)

print("\n================ REAÇÕES =================")
print("Somente aparecem nos GDL restringidos:\n")
print(reactions)
