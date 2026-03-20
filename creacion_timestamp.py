import pandas as pd

# Cargar dataset
df = pd.read_csv("tripadvisor_european_restaurants.csv")

# Fecha inicial
fecha_inicio = pd.Timestamp("2021-01-01 00:00:00")

# Crear la nueva columna timestamp según el orden de las filas
df["timestamp"] = fecha_inicio + pd.to_timedelta(range(len(df)), unit="m")

