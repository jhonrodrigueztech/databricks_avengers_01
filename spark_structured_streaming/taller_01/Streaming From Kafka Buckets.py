# Databricks notebook source
# org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3
from pyspark.sql.functions import *

key = "X4TCJ75W3DAP5KHJ"
secret = "gaAKphXY6BjGRi53T9qsvCEvku5X06S2AkvRLiaHpYWZnGrMSbdE7vYC0llo96rR"
server = "pkc-6vz38.westus2.azure.confluent.cloud:9092"

topic_name = "buckets"

schemaJson = "struct<dni:string,card_number:string,type_credit_card:string,ubicacion:string>"

checkpoint_path = "/FileStore/streaming/checkpoint/taller01/kafka/buckets"

dfAccounts = (spark.readStream.format("kafka")
                .option("subscribe", topic_name )
                .option("kafka.security.protocol", "SASL_SSL") 
                .option("kafka.sasl.jaas.config",
                        f"org.apache.kafka.common.security.plain.PlainLoginModule required username='{key}' password='{secret}';") 
                .option("kafka.sasl.mechanism", "PLAIN") 
                .option("kafka.bootstrap.servers", server) 
                .option("startingOffsets", "earliest") 
                .load()
                .withColumn("key", col("key").cast("string")  )
                .withColumn("value", col("value").cast("string")  )
                .withColumn("value", from_json( "value" , schemaJson )  )
                .select("key", "value.*", col("timestamp").alias("pauditTime"), "offset", "timestamp", "partition" , "topic")
                
         )

(
dfAccounts
    .writeStream
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path) 
    .toTable("dtw_avengers_lakehouse.bronze_dev.buckets_brz")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dtw_avengers_lakehouse.bronze_dev.buckets_brz
