# PRACTICA_SDPD2

Este archivo muestra y detalla los procesos y problemas con los que nos hemos ido encontrando durante la realización de la práctica.

## OBJETIVO

Como objetivo en esta práctica tenemos la creación de un *pipeline* en Airflow que automatice la limpieza y el proceso **ETL** del dataset sacado de Tripadvisor.

Tras balancear diferentes preguntas y cuestiones acerca de la **dirección** en la que enfocaremos nuestra práctica, como grupo hemos decidido que enfocaremos el estudio en crear un "ranking" de paises con mejores restaurantes calidad-precio.

Como buena práctica, dejaremos el enlace aquí para dar crédito al autor y que se tenga acceso a la descarga de los datos:

https://www.kaggle.com/datasets/stefanoleone992/tripadvisor-european-restaurants/data

## DATOS: TripAdvisor European restaurants

Este dataset contiene la información de más de un millón de restaurantes europeos extraída de TripAdvisor. A continuación, se detallan las variables de las 42 columnas principales, agrupadas por su naturaleza lógica:

**1. Identificación y Ubicación**
- `restaurant_link`: URL única del restaurante en la plataforma. Actúa como identificador único principal.

- `restaurant_name`: Nombre comercial del restaurante.

- `original_location`: Ubicación en texto libre tal y como aparece en la web (suele incluir ciudad, región y país).

- `country` / `region` / `province` / `city`: Desglose geográfico estructurado. Son variables categóricas clave para la agrupación de los datos.

- `address`: Dirección física completa del local.

`latitude` / `longitude`: Coordenadas geográficas exactas. (Críticas para visualizaciones geoespaciales).

**2. Características del Restaurante**
- `price_level`: Nivel de precio categorizado por la plataforma (suele representarse como $, $$-$$$, $$$$).

- `price_range`: Rango de precios estimado en formato texto.

- `meals`: Tipos de servicio de comida que ofrecen (ej. Desayuno, Comida, Cena, Brunch).

- `cuisines`: Tipo de cocina o gastronomía principal del local (Italiana, Mediterránea, Asiática, etc.).

- `special_diets`: Opciones dietéticas especiales mencionadas en el perfil.

- `features`: Características de infraestructura del local (Tiene terraza, acepta tarjetas, acceso para sillas de ruedas, Wi-Fi, etc.).

- `vegetarian_friendly`  / `vegan_options` / `gluten_free`: Indicadores binarios (Y/N) que confirman si el local ofrece este tipo de menús adaptados.

**3. Puntuaciones y Popularidad (Métricas de Calidad)**
- `avg_rating`: Puntuación media global otorgada por los usuarios (rango de 1.0 a 5.0 burbujas).

- `total_reviews_count`: Volumen total de opiniones registradas.

- `popularity_detailed`: Ranking exacto del restaurante dentro de su ciudad (ej. "Nº 3 de 500 restaurantes en Madrid").

- `excellent` / `very_good` / `average` / `poor` / `terrible`: Desglose del número absoluto de votos que el local ha recibido en cada nivel de satisfacción.

- `food` / `service` / `value` / `atmosphere`: Puntuación desglosada (de 1.0 a 5.0) en los cuatro pilares fundamentales: Comida, Servicio, Relación Calidad-Precio (Value) y Atmósfera.

**4. Horarios y Metadatos**
- `original_open_hours`: Cadena de texto en bruto con los horarios de apertura semanales.

- `open_days_per_week`: Número de días a la semana que el establecimiento está abierto al público.

- `open_hours_per_week`: Total de horas de operatividad a la semana.

- `keywords`: Palabras clave más repetidas extraídas automáticamente de las reseñas.

## EDA:

Para saber qué *tasks* deberemos incluir en el **pipeline**, nuestro primer paso será investigar los datos con el fin de entenderlos, gestionar valores atípicos y nulos, ver posibles transformaciones o reducciones de dimensionalidad, entre otras cosas.

Para ello, hemos creado un archivo `ipynb` para poder comentar todos los pasos y realizarlos en scripts de python.

## AIRFLOW

### TASK 0: CARGAR CONFIGURACIÓN (FUNCIÓN AUXILIAR)

En este bloque inicial preparamos la base para realizar correctamente el flujo de trabajo. Primero definimos una función auxiliar para cargar la configuración del proyecto desde un archivo externo, lo que nos permite separar los parámetros del código principal.

Después declaramos el DAG de Airflow, que será el encargado de orquestar el proceso ETL. En esta definición establecemos su identificador, indicamos que su ejecución será manual por el momento, fijamos una fecha de inicio y desactivamos las ejecuciones para evitar que se lancen procesos pendientes de fechas anteriores.

En conjunto, este fragmento deja creada la estructura general del pipeline antes de realizar las tareas de extracción, transformación y carga de datos (ETL).

### TASK 1: EXTRAER Y PREPARAR

En este fragmento definimos la primera tarea del pipeline, en la que realizamos la extracción y preparación de los datos. Para ello cargamos la configuración del proyecto, hecha en la task 0, y leemos el archivo CSV desde la ruta correcta. A continuación, nos quedamos únicamente con las variables más relevantes para el análisis, como el nombre del restaurante, el país, la ciudad, la valoración media, el nivel de precio y el número total de reseñas.

Después realizamos una limpieza básica eliminando los valores nulos, de forma que trabajemos solo con datos completos. Una vez limpiado el conjunto de datos, lo guardamos en un archivo temporal en formato Parquet, que resulta más eficiente para las siguientes etapas del flujo de trabajo. Por último, la tarea devuelve la ruta donde se encuentra ese archivo temporal, lo que permite que las tareas posteriores continúen el procesamiento a partir de unos datos ya filtrados y limpios.

### TASK 2: TRANSFORMAR

En esta segunda tarea del pipeline de flujo de trabajo realizamos la transformación de los datos que hemos limpiado y filtrado en la anterior tarea. Para ello cargamos el archivo temporal generado en la fase anterior y aplicamos una serie de operaciones orientadas a mejorar su utilidad. En primer lugar, transformamos la variable categórica asociada al nivel de precio en una representación numérica, lo que nos permite trabajar con ella de forma más sencilla.

A continuación, construimos una nueva variable derivada que relaciona la valoración media del restaurante con su nivel de precio, obteniendo así un indicador de calidad-precio. Después aplicamos un filtro de fiabilidad definido en el archivo de configuración, conservando únicamente aquellos registros que superan un número mínimo de reseñas. Finalmente, guardamos el conjunto de datos transformado en la ruta final que hemos indicado en la configuración, dejándolo preparado para su uso en etapas posteriores del proyecto.

### TASK 3: CARGA EN KAFKA

En esta tercera tarea del pipeline realizamos la fase de carga, enviando a Kafka un resumen de la información ya transformada. Para ello leemos el fichero procesado y, en lugar de enviar todos los registros de forma individual, agrupamos los datos por país para generar un resultado más manejable. En concreto, calculamos un ranking en función del indicador calidad-precio, lo que nos permite identificar los países mejor posicionados según esta métrica.

A continuación, construimos un mensaje en formato JSON que incluye información sobre el evento ejecutado, la ruta del archivo procesado y el ranking obtenido. Finalmente, nos conectamos a Kafka utilizando la configuración definida en el proyecto y enviamos dicho mensaje al tópico correspondiente. De este modo, dejamos disponible el resultado del pipeline para su consumo por otros sistemas o procesos.


























****
Autores:

- Alonso Rescalvo Casas
- Diego Rodríguez Monteagudo
- Adrián Gutiérrez Toledo
