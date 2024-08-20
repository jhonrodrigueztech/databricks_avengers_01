# Databricks notebook source
# MAGIC %sql
# MAGIC describe history dtw_avengers_lakehouse.silver_dev.messages_silver_v2

# COMMAND ----------

display(dbutils.fs.ls("/FileStore/streaming/checkpoint/delta/message_new_07/"))

# COMMAND ----------

display(spark.read.text("dbfs:/FileStore/streaming/checkpoint/delta/message_02/"))

# COMMAND ----------

display(spark.read.text("dbfs:/FileStore/streaming/checkpoint/delta/message_02/offsets/1"))

# COMMAND ----------

# MAGIC %sql
# MAGIC describe history dtw_avengers_lakehouse.bronze_dev.messages_kafka_brz

# COMMAND ----------

display(dbutils.fs.ls("/FileStore/streaming/checkpoint/delta/message_new_07/offsets/0"))

# COMMAND ----------

from pyspark.sql.functions import *

table = "dtw_avengers_lakehouse.bronze_dev.messages_kafka_brz"
checkpoint_path = "/FileStore/streaming/checkpoint/delta/message_new_07" # //

(
    spark.readStream
    .option("startingVersion", 7)
    .table(table)
    .select("ordertime", "orderid", "itemid", "timestamp" , current_timestamp().alias("processing_time"))
    .writeStream
    .trigger(processingTime="5 seconds") 
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path) 
    .toTable("dtw_avengers_lakehouse.silver_dev.messages_silver_v2")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dtw_avengers_lakehouse.silver_dev.messages_silver_v2
