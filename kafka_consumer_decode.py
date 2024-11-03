from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
from collections import deque

# Configuración del Consumer
KAFKA_SERVER = '164.92.76.15:9092'
TOPIC = '21826'

# Diccionario para mapear valores de bits a direcciones de viento
DIRECCIONES_VIENTO = {
    "N": 0, "NO": 1, "O": 2, "SO": 3,
    "S": 4, "SE": 5, "E": 6, "NE": 7
}

# Búsqueda inversa
DIRECCIONES_VIENTO_INV = {v: k for k, v in DIRECCIONES_VIENTO.items()}

# Configuración para almacenar datos y gráficos en vivo
all_temp = deque(maxlen=100)
all_hume = deque(maxlen=100)
all_wind = deque(maxlen=100)

# Función para decodificar datos de 3 bytes a JSON
def decode(payload):
    # Convertir de 3 bytes a un valor de 24 bits
    bits = int.from_bytes(payload, byteorder='big')

    # Extraer los datos usando máscaras de bits
    temperatura = (bits >> 10) & 0x3FFF
    humedad = (bits >> 3) & 0x7F
    direccion_viento = bits & 0x07

    # Restaurar valores originales
    temperatura = temperatura / 10.0
    direccion_viento_texto = DIRECCIONES_VIENTO_INV[direccion_viento]

    return {
        "temperatura": temperatura,
        "humedad": humedad,
        "direccion_viento": direccion_viento_texto
    }

# Configurar el consumidor
consumer = KafkaConsumer(
    TOPIC,
    group_id='grupo_consumidor',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda v: v
)

# Inicializar el gráfico
plt.ion()
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

def actualizar_grafico():
    ax1.clear()
    ax2.clear()
    ax3.clear()
    
    # Gráfico de temperatura
    ax1.plot(all_temp, label="Temperatura (°C)", color='red')
    ax1.set_ylabel("Temperatura (°C)")
    ax1.legend(loc='upper left')
    
    # Gráfico de humedad
    ax2.plot(all_hume, label="Humedad (%)", color='blue')
    ax2.set_ylabel("Humedad (%)")
    ax2.legend(loc='upper left')
    
    # Gráfico de dirección del viento
    ax3.plot(all_wind, label="Dirección del Viento", color='green', marker='o', linestyle='None')
    ax3.set_ylabel("Dirección del Viento")
    ax3.legend(loc='upper left')
    
    plt.draw()
    plt.pause(0.1)

# Consumir y graficar
try:
    for mensaje in consumer:
        data = decode(mensaje.value)
        print(f"Datos recibidos y decodificados: {data}")
        
        all_temp.append(data['temperatura'])
        all_hume.append(data['humedad'])
        all_wind.append(data['direccion_viento'])
        
        actualizar_grafico()

except KeyboardInterrupt:
    print("Consumo interrumpido.")

finally:
    plt.ioff()
    actualizar_grafico()
    plt.show()
