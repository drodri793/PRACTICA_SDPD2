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

- `vegetarian_friendly` / `vegan_options` / `gluten_free`: Indicadores binarios (Y/N) que confirman si el local ofrece este tipo de menús adaptados.

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


























****
Autores:

- Alonso Rescalvo Casas
- Diego Rodríguez Monteagudo
- Adrián Gutiérrez Toledo
