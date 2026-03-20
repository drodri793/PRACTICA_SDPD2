# PRACTICA_SDPD2

El objetio del trabajo es crear un DAG de operaciones de limpieza y preparación de datos a través de airflow.

Para empezar hemos creado una variable timestamp, ya que nuestro dataset no la contenía. Esta variable es simplemente para poder simular un procesamiento de datos en streaming, pero no se puede utilizar como una vbariable literal. Esta variable empieza en "01-01-2021 00:00:00" y va sumando un segundo a cada observación, sin que ninguna observación tenga el mismo timestamp.
