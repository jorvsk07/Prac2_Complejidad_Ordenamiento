import os
import pandas as pd
import matplotlib.pyplot as plt

dfs = []

# Cargar C++ si existe (convirtiendo KB a MB para homologar)
if os.path.exists("resultados_cpp.csv"):
    df_cpp = pd.read_csv("resultados_cpp.csv")
    df_cpp["Lenguaje"] = "C++"
    if "Memoria_KB" in df_cpp.columns:
        df_cpp["Memoria_MB"] = df_cpp["Memoria_KB"] / 1024.0
    dfs.append(df_cpp)

# Cargar Python si existe
if os.path.exists("resultados_python.csv"):
    df_py = pd.read_csv("resultados_python.csv")
    df_py["Lenguaje"] = "Python"
    dfs.append(df_py)

if not dfs:
    print("No se encontraron archivos CSV. Corre primero los benchmarks.")
    exit()

df = pd.concat(dfs, ignore_index=True)
df["Serie"] = df["Algoritmo"] + " (" + df["Lenguaje"] + ")"

# -------------------------------------------------------------
# Gráfica 1: Tiempo de Ejecución
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
for serie, grupo in df.groupby("Serie"):
    grupo = grupo.sort_values(by="Tamaño")
    plt.plot(grupo["Tamaño"], grupo["Tiempo_s"], marker="o", label=serie)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Longitud del Arreglo (N)", fontsize=11)
plt.ylabel("Tiempo de Ejecución (segundos)", fontsize=11)
plt.title("Comparativa de Tiempo de Ejecución (Escala Log-Log)", fontsize=13)
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("grafica_tiempos.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Gráfica 2: Consumo de Memoria
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
for serie, grupo in df.groupby("Serie"):
    grupo = grupo.sort_values(by="Tamaño")
    plt.plot(grupo["Tamaño"], grupo["Memoria_MB"], marker="s", linestyle="--", label=serie)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Longitud del Arreglo (N)", fontsize=11)
plt.ylabel("Memoria Consumida (MB)", fontsize=11)
plt.title("Comparativa de Consumo de Memoria (Escala Log-Log)", fontsize=13)
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("grafica_memoria.png", dpi=300)
plt.close()

print("¡Listo! Se generaron 'grafica_tiempos.png' y 'grafica_memoria.png'.")