# Databricks notebook source
from pyspark.sql.functions import *

# COMMAND ----------

dfVehiclesRT = spark.readStream.table("dtw_avengers_lakehouse.bronze_dev.vehicles_bronze") 
dfPassengersByVehicleRT = spark.readStream.table("dtw_avengers_lakehouse.bronze_dev.pasajeros")

# COMMAND ----------

dfStreamingJoin =( dfVehiclesRT
                    .join(dfPassengersByVehicleRT,
                           dfVehiclesRT.id == dfPassengersByVehicleRT.idcar))

display(dfStreamingJoin)
