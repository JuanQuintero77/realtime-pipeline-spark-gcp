from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

spark = (SparkSession.builder
         .appName("StreamingApp")
         .getOrCreate()
    )

schema = StructType([
    StructField("event_id", StringType()),
    StructField("event_type", StringType()),
    StructField("source", StringType()),
    StructField("event_timestamp", StringType()),         
    StructField("ingestion_timestamp", StringType()),
    StructField("payload", StructType([
        StructField("user_id", StringType(), True),
        StructField("order_id", StringType(), True),
        StructField("total_amount", DoubleType(), True),
        StructField("email", StringType(), True),
        StructField("name", StringType(), True),
        StructField("payment_method", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("product_id", StringType(), True),
        StructField("category", StringType(), True),
    ]))
])

df = (spark.readStream
      .format("text")
      .option("recursiveFileLookup", "true")
      .load("data/raw/events")
    )

df = df.withColumn("parsed", from_json("value", schema)).select("parsed.*")

df_transformed = (df
                  .withColumn("event_timestamp", to_timestamp(col("event_timestamp")))
                  .withColumn("ingestion_timestamp", to_timestamp(col("ingestion_timestamp"))))

query = (df_transformed.writeStream
         .format("parquet")
         .option("path", "data/bronze/events")
         .option("checkpointLocation", "data/checkpoint/events")
         .outputMode("append")
         .start()
         )

query.awaitTermination()