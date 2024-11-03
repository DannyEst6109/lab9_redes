from kafka import KafkaProducer
import json
import random
import time

# Configuración del servidor Kafka
KAFKA_SERVER = '164.92.76.15:9092'
TOPIC = '21826'

# Inicialización del productor Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Función para generar datos simulados de sensores con distribución gaussiana
def generar_datos():
    temperatura = max(0, min(110, round(random.gauss(55, 15), 2)))
    humedad = max(0, min(100, int(random.gauss(50, 10))))
    direccion_viento = random.choice(["N", "NO", "O", "SO", "S", "SE", "E", "NE"])
    
    return {
        "temperatura": temperatura,
        "humedad": humedad,
        "direccion_viento": direccion_viento
    }

# Enviar datos cada 15-30 segundos
try:
    while True:
        data = generar_datos()
        producer.send(TOPIC, value=data)
        print(f"Datos enviados: {data}")
        time.sleep(random.randint(5, 15))
except KeyboardInterrupt:
    print("Producción interrumpida")
finally:
    producer.close()
