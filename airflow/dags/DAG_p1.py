import json
import tomllib
from datetime import datetime
from airflow.decorators import dag, task
from kafka import KafkaProducer

# ==========================================
# FUNCIÓN AUXILIAR: Cargar Configuración
# ==========================================
def load_config():
    # Asegúrate de que esta ruta coincida con donde guardaste tu config.toml
    with open("/home/vboxuser/SDPD2/airflow/dags/config.toml", "rb") as f:
        return tomllib.load(f)

# ==========================================
# DEFINICIÓN DEL DAG (Sintaxis TaskFlow)
# ==========================================
@dag(
    dag_id="tripadvisor_etl_ranking",
    schedule_interval=None, # Ejecución manual por ahora
    start_date=datetime(2026, 3, 26),
    catchup=False,
    tags=["sdpd2", "etl", "tripadvisor"]
)
def tripadvisor_pipeline():

    # ------------------------------------------
    # TAREA 1: EXTRAER Y PREPARAR (Extract & Clean)
    # ------------------------------------------
    @task
    def extract_and_prepare() -> str:
        config = load_config()
        
        # Lectura de alto rendimiento con pyarrow
        print("Leyendo CSV en crudo...")
        df = pd.read_csv(config["paths"]["raw_csv"], engine="pyarrow")
        
        # Filtrado de columnas útiles
        columnas = ['restaurant_name', 'country', 'city', 'avg_rating', 'price_level', 'total_reviews_count']
        df = df[columnas]
        
        # Limpieza de nulos
        df = df.dropna()
        
        # Guardamos en un archivo temporal ultrarrápido y devolvemos la ruta
        tmp_path = "/tmp/t1_prepared.parquet"
        df.to_parquet(tmp_path, engine="pyarrow")
        print(f"✅ Datos limpios guardados en: {tmp_path}")
        
        return tmp_path

    # ------------------------------------------
    # TAREA 2: TRANSFORMAR (Transform)
    # ------------------------------------------
    @task
    def transform_data(input_path: str) -> str:
        config = load_config()
        df = pd.read_parquet(input_path, engine="pyarrow")
        
        # Tratamiento de variables categóricas (mapeo de euros)
        mapa_precios = {'€': 1, '€€ - €€€': 2, '€€€€': 3}
        df['price_level_num'] = df['price_level'].map(mapa_precios)
        
        # Transformación de variables: Creación del KPI
        df['score_calidad_precio'] = df['avg_rating'] / df['price_level_num']
        
        # Filtro de fiabilidad desde el TOML
        min_rev = config["processing"]["min_reviews_count"]
        df = df[df['total_reviews_count'] >= min_rev]
        
        # Guardar resultado final
        final_path = config["paths"]["processed_parquet"]
        df.to_parquet(final_path, engine="pyarrow")
        print(f"✅ Datos transformados guardados en: {final_path}")
        
        return final_path

    # ------------------------------------------
    # TAREA 3: CARGA EN KAFKA (Load)
    # ------------------------------------------
    @task
    def load_to_kafka(input_path: str):
        config = load_config()
        df = pd.read_parquet(input_path, engine="pyarrow")
        
        # Agrupamos la info para no saturar Kafka enviando un millón de filas.
        # Enviamos el Top 10 de países con mejor Calidad-Precio
        ranking = df.groupby('country')['score_calidad_precio'].mean().sort_values(ascending=False).head(10)
        
        # Construimos el mensaje JSON
        mensaje = {
            "evento": "pipeline_completado",
            "archivo_destino": input_path,
            "top_10_paises_calidad_precio": ranking.to_dict()
        }
        
        # Nos conectamos a Kafka y enviamos el mensaje
        producer = KafkaProducer(
            bootstrap_servers=config["kafka"]["bootstrap_servers"],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        producer.send(config["kafka"]["topic_name"], value=mensaje)
        producer.flush()
        print(f"🚀 Mensaje enviado a Kafka: {mensaje}")

    # ==========================================
    # SECUENCIA DE EJECUCIÓN DEL DAG
    # ==========================================
    # Aquí definimos el orden estricto: T1 -> T2 -> T3
    ruta_preparada = extract_and_prepare()
    ruta_transformada = transform_data(ruta_preparada)
    load_to_kafka(ruta_transformada)

# Instanciar el DAG
dag_instance = tripadvisor_pipeline()