from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofmonth

# ------------------------
# Spark Session
# ------------------------
spark = (
    SparkSession.builder
    .appName("SilverApp")
    .getOrCreate()
)

# ------------------------
# Infer Schema from Bronze
# ------------------------
static_df = spark.read.parquet("data/bronze/events")
schema = static_df.schema


# ------------------------
# Read Bronze (stream)
# ------------------------
df = (
    spark.readStream
    .format("parquet")
    .schema(schema)
    .load("data/bronze/events")
)

# ------------------------
# USERS
# ------------------------
users_df = (
    df
    .filter(col("event_type") == "user_created")
    .select(
        col("event_id"),
        col("event_timestamp"),
        col("ingestion_timestamp"),
        col("source"),
        col("payload.user_id").alias("user_id"),
        col("payload.email").alias("email"),
        col("payload.name").alias("name"),
    )
    .withColumn("year", year("event_timestamp"))
    .withColumn("month", month("event_timestamp"))
    .withColumn("day", dayofmonth("event_timestamp"))
)

# ------------------------
# PRODUCT VIEWS
# ------------------------
product_views_df = (
    df
    .filter(col("event_type") == "product_viewed")
    .select(
        col("event_id"),
        col("event_timestamp"),
        col("ingestion_timestamp"),
        col("source"),
        col("payload.user_id").alias("user_id"),
        col("payload.product_id").alias("product_id"),
        col("payload.category").alias("category"),
    )
    .withColumn("year", year("event_timestamp"))
    .withColumn("month", month("event_timestamp"))
    .withColumn("day", dayofmonth("event_timestamp"))
)

# ------------------------
# ORDERS
# ------------------------
orders_df = (
    df
    .filter(col("event_type") == "order_created")
    .select(
        col("event_id"),
        col("event_timestamp"),
        col("ingestion_timestamp"),
        col("source"),
        col("payload.user_id").alias("user_id"),
        col("payload.order_id").alias("order_id"),
        col("payload.total_amount").alias("total_amount"),
    )
    .withColumn("year", year("event_timestamp"))
    .withColumn("month", month("event_timestamp"))
    .withColumn("day", dayofmonth("event_timestamp"))
)

# ------------------------
# PAYMENTS
# ------------------------
payments_df = (
    df
    .filter(col("event_type") == "payment_completed")
    .select(
        col("event_id"),
        col("event_timestamp"),
        col("ingestion_timestamp"),
        col("source"),
        col("payload.user_id").alias("user_id"),
        col("payload.order_id").alias("order_id"),
        col("payload.amount").alias("amount"),
        col("payload.payment_method").alias("payment_method"),
    )
    .withColumn("year", year("event_timestamp"))
    .withColumn("month", month("event_timestamp"))
    .withColumn("day", dayofmonth("event_timestamp"))
)

# ------------------------
# WRITE STREAMS
# ------------------------

users_query = (
    users_df.writeStream
    .format("parquet")
    .option("path", "data/silver/users")
    .option("checkpointLocation", "data/checkpoints/silver_users")
    .partitionBy("year", "month", "day")
    .outputMode("append")
    .start()
)

product_views_query = (
    product_views_df.writeStream
    .format("parquet")
    .option("path", "data/silver/product_views")
    .option("checkpointLocation", "data/checkpoints/silver_product_views")
    .partitionBy("year", "month", "day")
    .outputMode("append")
    .start()
)

orders_query = (
    orders_df.writeStream
    .format("parquet")
    .option("path", "data/silver/orders")
    .option("checkpointLocation", "data/checkpoints/silver_orders")
    .partitionBy("year", "month", "day")
    .outputMode("append")
    .start()
)

payments_query = (
    payments_df.writeStream
    .format("parquet")
    .option("path", "data/silver/payments")
    .option("checkpointLocation", "data/checkpoints/silver_payments")
    .partitionBy("year", "month", "day")
    .outputMode("append")
    .start()
)

# ------------------------
# KEEP STREAMING ALIVE
# ------------------------
spark.streams.awaitAnyTermination()