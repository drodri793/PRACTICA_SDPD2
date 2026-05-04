from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# 1. Crear la sesión de Spark 
spark = SparkSession.builder \
    .appName("ConsultasEntregable3") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Conectar a Kafka y leer el stream desde el principio (earliest)
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "purchases") \
    .option("startingOffsets", "earliest") \
    .load()

# Convertir los datos binarios de Kafka a texto normal
parsed_df = df.selectExpr("CAST(value AS STRING) as value")

# =========================================================================
# CONSULTA 1: Modo APPEND
# Objetivo: Leer los datos en crudo y guardarlos tal cual van llegando.
# =========================================================================

def escribir_salida1(batch_df, batch_id):
    filas = batch_df.collect()
    if filas:
        # Abrimos en modo "a" (append) para añadir líneas al final del fichero
        with open("salida1.txt", "a", encoding="utf-8") as f:
            for fila in filas:
                f.write(f"NUEVO MENSAJE RECIBIDO: {fila['value']}\n")

query1 = parsed_df.writeStream \
    .outputMode("append") \
    .foreachBatch(escribir_salida1) \
    .start()

# =========================================================================
# CONSULTA 2: Modo COMPLETE
# Objetivo: contar cuántas veces se ha vendido cada producto.
# =========================================================================

# Agrupamos por producto y contamos las ocurrencias
conteo_df = parsed_df.groupBy("value").count()

def escribir_salida2(batch_df, batch_id):
    filas = batch_df.collect()
    if filas:
        # Abrimos en modo "w" (overwrite) porque el modo complete recalcula TODO 
        # y queremos que el archivo texto tenga siempre la tabla actualizada.
        with open("salida2.txt", "w", encoding="utf-8") as f:
            f.write("RESUMEN DE VENTAS (MODO COMPLETE)\n")
            f.write("-" * 35 + "\n")
            f.write("PRODUCTO \t\t| CANTIDAD TOTAL\n")
            f.write("-" * 35 + "\n")
            for fila in filas:
                f.write(f"{fila['value']} \t\t| {fila['count']}\n")

query2 = conteo_df.writeStream \
    .outputMode("complete") \
    .foreachBatch(escribir_salida2) \
    .start()

# 3. Mantener el script corriendo hasta que lo paremos manualmente
print("Las consultas se están ejecutando. Revisa los archivos salida1.txt y salida2.txt.")
print("Pulsa Ctrl+C para detener el proceso.")
spark.streams.awaitAnyTermination()