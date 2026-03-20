import pandas as pd

# 1. Cargar los datos (apuntamos a donde lo moviste antes)
archivo = 'airflow/dags/tripadvisor_european_restaurants.csv'
print(f"\n--- INICIANDO RADIOGRAFÍA DE: {archivo} ---\n")

try:
    df = pd.read_csv(archivo)
except FileNotFoundError:
    print("❌ ERROR: No encuentro el archivo. ¿Seguro que está en esa ruta?")
    exit()

# 2. Tamaño del dataset
print("TAMAÑO DEL DATASET:")
print(f"Total de restaurantes (filas): {df.shape[0]}")
print(f"Total de variables (columnas): {df.shape[1]}\n")

# 3. Análisis de Nulos (Vital para tu memoria del proyecto)
print("VALORES NULOS POR COLUMNA:")
nulos = df.isnull().sum()
nulos_porcentaje = (nulos / len(df)) * 100
resumen_nulos = pd.DataFrame({'Total Nulos': nulos, 'Porcentaje (%)': nulos_porcentaje})
# Filtramos para mostrar solo las columnas que tienen algún nulo
print(resumen_nulos[resumen_nulos['Total Nulos'] > 0].sort_values(by='Porcentaje (%)', ascending=False))
print("\n")

# 4. Tipos de datos
print("TIPOS DE DATOS DE LAS COLUMNAS:")
print(df.dtypes)
print("\n")

# 5. Muestra de la primera fila (para ver qué pinta tienen los datos)
print("EJEMPLO DE UN REGISTRO (Fila 1):")
print(df.iloc[0])
print("\n--- FIN DE LA RADIOGRAFÍA ---")