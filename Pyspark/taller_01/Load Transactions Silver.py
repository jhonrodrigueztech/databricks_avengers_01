# Databricks notebook source
dni: "8744566"
mount: 540.36
to_person: "9856634"

# COMMAND ----------

from pyspark.sql.functions import *

dfKafkaBronze = spark.sql(
                          f"""
                          select value:dni , value:mount, value:to_person
                          from dtw_avengers_lakehouse.bronze_dev.transactions_kafka
                          """
                          )
dfClean = (dfKafkaBronze
    .withColumn("dni", translate(col("dni"), "\"" , "")  )
    .withColumn("to_person", translate(col("to_person"), "\"" , "")  )
    .withColumn("mount", col("mount").cast("double") ))

dfSendedByDni = spark.sql(
    f"""
        select dni, sum(mount) as sended , count("*") as total_sended
        from {{df}}
        group by dni
    """ , df = dfClean
)

dfReceived = (dfClean
            .groupBy("to_person")
            .agg( 
                sum("mount").alias("received") ,
                count("*").alias("total_received")  )
            .withColumnRenamed("to_person", "dni")
            .where(col("dni").isNotNull()))


# COMMAND ----------

display(dfReceived)

# COMMAND ----------

dfFinal2 =  ( dfReceived.join(dfSendedByDni,
                                      ["dni"] , 
                                      "full_outer")
                     .na.fill(0)
                     .withColumn("total", col("total_received") + col("total_sended"))
                     .drop("total_sended", "total_received")
                     
                     )

# COMMAND ----------

display(dfFinal2)

# COMMAND ----------

dfFinal = dfReceived.alias("r").join(dfSendedByDni.alias("s")   ,
                                      col("r.to_person") == col("s.dni") , 
                                      "left")

# COMMAND ----------

display(dfFinal)

# COMMAND ----------

display(dfFinal)

# COMMAND ----------

display(dfReceived)

# COMMAND ----------

display(dfSendedByDni)

# COMMAND ----------

display(dfClean)
