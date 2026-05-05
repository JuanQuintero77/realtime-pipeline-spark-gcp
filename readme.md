# 🚀 Proyecto End-to-End Data Engineering (Spark + dbt + GCP)

## 🎯 Objetivo

Construir un pipeline completo de ingeniería de datos que simule un sistema real de eventos:

* Generación de datos (streaming simulado)
* Procesamiento con Spark
* Modelado con dbt
* Infraestructura con Terraform
* (Fase futura) ML sobre datos procesados

---

# 🧱 Arquitectura General

```
[Generator (Docker)]
        ↓
   data/raw (JSONL)
        ↓
   Spark (Streaming)
        ↓
   Bronze (Parquet)
        ↓
   Silver (Transformaciones)
        ↓
   Gold (dbt models)
        ↓
   (Opcional) ML / Analytics
```

---

# ⚙️ FASE 0 — Setup del entorno

## Requisitos

* WSL2 (Linux)
* Python 3.10+
* Docker (instalado dentro de WSL)
* Java (OpenJDK 11 o 17)
* PySpark

---

## 🔹 Configuración crítica

### Instalar Java

```bash
sudo apt update
sudo apt install openjdk-11-jdk -y
```

### Configurar JAVA_HOME

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

Persistir:

```bash
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc
```

---

# 📦 FASE 1 — Generador de datos (Ingestion)

## Estructura

```
ingestion/
├── generator.py
├── event_builder.py
├── config.py
```

---

## 🔹 Concepto

Simular eventos tipo:

* user_created
* product_viewed
* order_created
* payment_completed

---

## 🔹 Características clave

* JSON Lines (`.jsonl`)
* Micro-batching
* Particionado por fecha
* Datos correlacionados (user_id, order_id)
* Distribución realista de eventos

---

## 🔹 Salida

```
data/raw/events/YYYY/MM/DD/HH/*.jsonl
```

---

## 🔹 Buenas prácticas aplicadas

* Separación de responsabilidades
* Payload dinámico por evento
* Timestamps realistas
* Simulación de streaming

---

# 🐳 FASE 2 — Dockerización

## 🔹 Objetivo

Ejecutar el generador como un contenedor desacoplado.

---

## Dockerfile

```
docker/ingestion/Dockerfile
```

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingestion/ ingestion/

CMD ["python", "ingestion/generator.py"]
```

---

## 🔹 Build

```bash
docker build -t ingestion-generator -f docker/ingestion/Dockerfile .
```

---

## 🔹 Run (CRÍTICO)

```bash
docker run -v $(pwd)/data:/app/data ingestion-generator
```

---

## 🧠 Concepto clave

* `/app/data` (contenedor)
* `./data` (host)

👉 Se conectan mediante volumen

---

# ⚡ FASE 3 — Spark Streaming

## 🔹 Objetivo

Leer eventos como streaming desde archivos.

---

## Archivo

```
spark/streaming.py
```

---

## 🔹 Inicialización

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("StreamingEvents").getOrCreate()
```

---

## 🔹 Lectura

```python
df = (
    spark.readStream
    .format("json")
    .option("recursiveFileLookup", "true")
    .load("data/raw/events")
)
```

---

## 🔹 Output (debug)

```python
query = (
    df.writeStream
    .format("console")
    .outputMode("append")
    .start()
)

query.awaitTermination()
```

---

## 🧠 Concepto clave

Simulación de streaming mediante llegada de archivos.

---

# 🥉 FASE 4 — Bronze Layer

## 🔹 Objetivo

Persistir datos crudos en formato optimizado.

---

## 🔹 Salida

* Formato: Parquet
* Ubicación: `data/bronze/`

---

## 🔹 Características

* Sin transformaciones
* Esquema base
* Alta fidelidad al raw

---

# 🥈 FASE 5 — Silver Layer

## 🔹 Objetivo

Limpiar y estructurar datos.

---

## 🔹 Transformaciones

* Flatten de `payload`
* Tipado de columnas
* Filtrado de errores
* Normalización

---

## 🔹 Ejemplo

```
event_type → columnas específicas
payload.user_id → user_id
```

---

# 🥇 FASE 6 — Gold Layer (dbt)

## 🔹 Objetivo

Modelado analítico.

---

## 🔹 Ejemplos de modelos

* users
* orders
* payments
* metrics

---

## 🔹 Herramienta

* dbt

---

## 🔹 Output

Tablas listas para:

* BI
* ML
* reporting

---

# ☁️ FASE 7 — GCP (Infraestructura)

## 🔹 Servicios

* Cloud Storage (raw/bronze)
* BigQuery (silver/gold)
* Dataflow o Dataproc (Spark)
* Composer (orquestación)

---

## 🔹 Terraform

Infraestructura como código:

* buckets
* datasets
* IAM
* pipelines

---

# 🤖 FASE 8 — Machine Learning (Opcional)

## 🔹 Enfoque correcto

ML sobre datos procesados (Gold)

---

## 🔹 Casos de uso

* fraude (payments)
* recomendaciones
* churn prediction

---

## 🔹 Flujo

```
Gold → Features → Model → Predictions
```

---

# 🧠 Buenas prácticas generales

* No mezclar lógica (modularidad)
* Usar particionado por fecha
* Evitar archivos gigantes
* Usar formatos columnar (Parquet)
* Separar compute de storage
* Versionar dependencias

---

# 🚀 Estado actual del proyecto

✔ Generador de eventos realista
✔ Docker funcionando
✔ Volúmenes configurados
✔ Datos persistiendo
✔ Base lista para Spark

---

# 🔜 Próximos pasos

1. Validar Spark streaming
2. Implementar Bronze layer
3. Construir Silver transformations
4. Integrar dbt
5. Subir a GCP
6. (Opcional) agregar ML

---

# 🧠 Resultado final

Proyecto tipo:

👉 Data Engineer (nivel profesional)

Con stack:

* Python
* Spark
* dbt
* Docker
* Terraform
* GCP

---

# 📌 Nota final

Este proyecto está diseñado para:

✔ Aprender arquitectura real
✔ Simular sistemas productivos
✔ Construir portafolio sólido

No es un tutorial — es un sistema.

---
