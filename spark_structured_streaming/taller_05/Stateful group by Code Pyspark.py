# Databricks notebook source
from pyspark.sql.functions import *

# COMMAND ----------

dfBronzeStreaming = ( spark
                        .readStream
                        .table("dtw_avengers_lakehouse.bronze_dev.vehicles_from_mainstreet")
                        .withWatermark("ts_auto" , "60 seconds")
                        .groupBy(
                            window("ts_auto", "30 seconds"),
                            "color"
                            )
                        .agg(sum("count_passenger").alias("total_pasajeros"))
                          .select("window.*" , "color" , "total_pasajeros")
                          .withColumn("start", date_format(col("start"), "MM/dd/yyyy hh:mm:ss" ) )
                         .withColumn("end", date_format(col("end"), "MM/dd/yyyy hh:mm:ss" ) )
                    )


# display(dfBronzeStreaming)

checkpoint_path = f"/FileStore/streaming/checkpoint/silver/taller06/stateful"

(
    dfBronzeStreaming
        .withColumn("execution_ts", date_format(current_timestamp(), "MM/dd/yyyy hh:mm:ss" ))
        .writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_path   )
        .toTable("dtw_avengers_lakehouse.silver_dev.contador_pasajeros_por_color_carro_v2")   
)   

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dtw_avengers_lakehouse.silver_dev.contador_pasajeros_por_color_carro_v2

# COMMAND ----------

#Para que sepa donde se ha quedado y cual ha sido su ultima carga a nivel de intervalo de tiempo
display(
    spark.read.format("statestore")
        .load("/FileStore/streaming/checkpoint/silver/taller06/stateful")
        .select("key.*" , "value" , "partition_id")
        .withColumn("start", date_format(col("window.start"), "MM/dd/yyyy hh:mm:ss" ) )
        .withColumn("end", date_format(col("window.end"), "MM/dd/yyyy hh:mm:ss" ) )
        .drop("window")
    )
