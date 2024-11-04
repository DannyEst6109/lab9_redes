# Proyecto de IoT con Apache Kafka
Este proyecto consiste en un laboratorio de IoT donde se utilizan Apache Kafka y Python para enviar y recibir datos meteorológicos en tiempo real. Los datos incluyen temperatura, humedad y dirección del viento. El laboratorio está dividido en dos programas: el productor y el consumidor de Kafka, que se encargan de simular y graficar los datos recibidos, respectivamente.

## Requisitos
- Python 3.8+
- Apache Kafka: Necesitas un servidor Kafka en funcionamiento (el proyecto utiliza la dirección 164.92.76.15:9092 para el servidor).
- Librerías de Python: Instala las siguientes librerías antes de ejecutar el proyecto:
```bash
pip install kafka-python
pip install matplotlib
```

## Instalación
1. Clona este repositorio en tu máquina local:
```bash
git clone https://github.com/DannyEst6109/lab9_redes
```
2. Asegúrate de tener las librerías necesarias y un servidor Kafka operativo.

## Ejecución
1. Ejecución del productor
Este programa genera datos meteorológicos simulados de temperatura, humedad y dirección del viento, y los envía al servidor Kafka.

```bash
python kafka_producer.py
```
El productor enviará un mensaje cada 5 a 15 segundos al servidor Kafka. Puedes ver en la consola los datos enviados en formato JSON.

2. Ejecución del consumidor
Este programa se conecta al servidor Kafka, consume los datos enviados por el productor y los grafica en tiempo real.

```bash
python kafka_consumer.py
```
El consumidor mostrará los datos recibidos y actualizará un gráfico en vivo con tres subgráficos:
- Temperatura (°C)
- Humedad (%)
- Dirección del viento

Para detener cualquiera de los programas, presiona Ctrl + C.

## Detalles del Proyecto
1. Productor: Genera datos utilizando una distribución gaussiana para simular valores de temperatura y humedad. La dirección del viento se selecciona aleatoriamente entre ocho direcciones. Los datos se serializan en JSON y se envían al tema 21826 en el servidor Kafka configurado.
2. Consumidor: Escucha el tema 21826 y procesa los mensajes en tiempo real. Los datos de temperatura, humedad y dirección del viento se almacenan en una cola de longitud fija para representar un histórico reciente y se grafican utilizando matplotlib.

Este proyecto también cubre preguntas sobre las ventajas de usar JSON y Apache Kafka en aplicaciones IoT, así como el enfoque de diseño Pub/Sub en Kafka. La presentación explica cómo se realiza la comunicación en Kafka y cómo se implementa una restricción de payload de 3 bytes en escenarios donde sea necesario comprimir la información meteorológica en formatos limitados, utilizando encoding y decoding específicos para optimizar el tamaño del mensaje.

## Notas
Asegúrate de que el servidor Kafka esté en ejecución y que tanto el productor como el consumidor estén conectados al mismo tema (21826).
