# Databricks notebook source
from pyspark.sql.functions import *

# COMMAND ----------

# dfVehiclesRT = spark.readStream.table("dtw_avengers_lakehouse.bronze_dev.vehicles_bronze") 
# dfPassengersByVehicleRT = spark.table("dtw_avengers_lakehouse.bronze_dev.pasajeros")

# dfVehiclesRT.join( dfPassengersByVehicleRT , "id = idcard")


# COMMAND ----------

from pyspark.sql.functions import *

dfVehiclesRT = (spark
                .readStream
                .table("dtw_avengers_lakehouse.bronze_dev.vehicles_bronze")
                .withWatermark("ts_auto", "2 minutes"))

dfPassengersByVehicleRT = (spark
                            .readStream
                            .table("dtw_avengers_lakehouse.bronze_dev.pasajeros")
                            .withWatermark("ts_message", "20 seconds"))

# COMMAND ----------

dfStreamingJoin =( dfVehiclesRT
                    .join(dfPassengersByVehicleRT,
                          
                           expr(""" 
                                id == idcar and
                                ts_message >= ts_auto and
                                ts_message <= ts_auto + interval 2 minutes
                                """)
                           
                           ))

(
    dfStreamingJoin.writeStream
            .format("delta")
            .option("checkpointLocation", "/FileStore/contracts/checkpoint/statefull/join/2308/v2")
            .outputMode("append")
       #      .trigger(processingTime='5 seconds')
            .toTable("dtw_avengers_lakehouse.silver_dev.table_stateful")
)

# COMMAND ----------


