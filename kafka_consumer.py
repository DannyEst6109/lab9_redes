from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
from collections import deque

# Configuración del Consumer
KAFKA_SERVER = '164.92.76.15:9092'
TOPIC = '21826'

# Configuración para almacenar datos y gráficos en vivo
all_temp = deque(maxlen=100)
all_hume = deque(maxlen=100)
all_wind = deque(maxlen=100)

# Configurar el consumidor
consumer = KafkaConsumer(
    TOPIC,
    group_id='grupo_consumidor',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
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
        data = mensaje.value
        print(f"Recibido: {data}")
        
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
