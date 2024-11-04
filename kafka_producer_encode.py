from kafka import KafkaProducer
import json
import random
import time

# Configuración del servidor Kafka
KAFKA_SERVER = '164.92.76.15:9092'
TOPIC = '21864'

# Diccionario para mapear direcciones del viento a valores de 3 bits
DIRECCIONES_VIENTO = {
    "N": 0, "NO": 1, "O": 2, "SO": 3,
    "S": 4, "SE": 5, "E": 6, "NE": 7
}

# Función para generar datos simulados de sensores con distribución gaussiana
def generar_datos():
    temperatura = max(0, min(110, round(random.gauss(55, 15), 1)))
    humedad = max(0, min(100, int(random.gauss(50, 10))))
    direccion_viento = random.choice(list(DIRECCIONES_VIENTO.keys()))
    
    return {
        "temperatura": temperatura,
        "humedad": humedad,
        "direccion_viento": direccion_viento
    }

# Función para codificar datos JSON a un payload de 3 bytes
def encode(data):
    temperatura = int(data["temperatura"] * 10)
    humedad = data["humedad"]
    direccion_viento = DIRECCIONES_VIENTO[data["direccion_viento"]]

    # Crear un valor de 24 bits concatenando los valores
    payload = (temperatura << 10) | (humedad << 3) | direccion_viento

    # Convertir a 3 bytes
    return payload.to_bytes(3, byteorder='big')

# Inicialización del productor Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: v
)

# Enviar datos cada 15-30 segundos
try:
    while True:
        data = generar_datos()
        encoded_data = encode(data)
        producer.send(TOPIC, value=encoded_data)
        print(f"Datos enviados (codificados): {encoded_data}")
        time.sleep(random.randint(5, 15))
except KeyboardInterrupt:
    print("Producción interrumpida")
finally:
    producer.close()
