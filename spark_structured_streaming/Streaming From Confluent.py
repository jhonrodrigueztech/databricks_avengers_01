# Databricks notebook source
# org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3
from pyspark.sql.functions import *

key = "X4TCJ75W3DAP5KHJ"
secret = "gaAKphXY6BjGRi53T9qsvCEvku5X06S2AkvRLiaHpYWZnGrMSbdE7vYC0llo96rR"
server = "pkc-6vz38.westus2.azure.confluent.cloud:9092"
topic_name = "new_messages"

schemaJson = "struct<ordertime:bigint,orderid:int,itemid:string>"

checkpoint_path = "/FileStore/streaming/checkpoint/kafka/messages_r1"

offeset= """{"new_messages":{"0":9}}"""

dfKafka = (spark.readStream.format("kafka")
                .option("subscribe", topic_name )
                .option("kafka.security.protocol", "SASL_SSL") 
                .option("kafka.sasl.jaas.config",
                        f"org.apache.kafka.common.security.plain.PlainLoginModule required username='{key}' password='{secret}';") 
                .option("kafka.sasl.mechanism", "PLAIN") 
                .option("kafka.bootstrap.servers", server) 
                # .option("startingOffsets", "earliest") 
                .option("startingOffsets", offeset) 
                .load()
                .withColumn("key", col("key").cast("string")  )
                .withColumn("value", col("value").cast("string")  )
                .withColumn("value", from_json( "value" , schemaJson )  )
                .select("key", "value.*", col("timestamp").alias("pauditTime"), "offset", "timestamp", "partition" , "topic")
                
         )

(
dfKafka
    .writeStream
    .trigger(processingTime="5 seconds") 
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path) 
    .toTable("dtw_avengers_lakehouse.bronze_dev.messages_kafka_brz")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC describe history dtw_avengers_lakehouse.bronze_dev.messages_kafka_brz

# COMMAND ----------

offeset = spark.read.text(f"/FileStore/streaming/checkpoint/kafka/messages_01/offsets/1").where("value like '%new_messages%'").collect()[0][0] 

print(offeset)

# COMMAND ----------

display(spark.read.text(f"/FileStore/streaming/checkpoint/kafka/messages_01/offsets/0"))

# COMMAND ----------

display(dbutils.fs.ls("/FileStore/streaming/checkpoint/kafka/messages_01/offsets"))

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dtw_avengers_lakehouse.bronze_dev.messages_kafka_brz
