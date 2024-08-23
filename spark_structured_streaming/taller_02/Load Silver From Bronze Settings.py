# Databricks notebook source
from pyspark.sql.functions import *

# COMMAND ----------

def getLastUpdateRow(df):

    from pyspark.sql.window import Window

    windowSpec =  Window.partitionBy("dni").orderBy(col("timestamp").desc())

    return ( df.withColumn("rankeo" , row_number().over(windowSpec) )
               .where("rankeo  == 1")
               .drop("rankeo")
                    )

# COMMAND ----------


table = "dtw_avengers_lakehouse.bronze_dev.settings_brz"
checkpoint_path = f"/FileStore/streaming/checkpoint/silver/taller02/settings"

dfAccounts = (
        spark.readStream.table(table)
                     .withColumn("settings" , 
                                 struct(col("color_background").alias("background"), "photo", "letter_size", "avatar_name"))
                    .select("dni", "settings" , "timestamp")
                    .withColumn("processing_time" ,  current_timestamp())
    )

from delta.tables import *


def workingWithMicroBatch(dfMicroBatch, id):
    
    df_registros_unicos = dfMicroBatch.transform(getLastUpdateRow).drop("timestamp")

    main_table = DeltaTable.forName(spark, "dtw_avengers_lakehouse.silver_dev.accounts_main_silver")

    (
        main_table.alias("source")
            .merge(df_registros_unicos.alias("inn"), "source.dni = inn.dni")
            .withSchemaEvolution()
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
    )

(
    dfAccounts
        .writeStream
        .trigger(processingTime='10 seconds') 
        .outputMode("update")
        .option("checkpointLocation", checkpoint_path) 
        .foreachBatch(workingWithMicroBatch)
        .start()
)


