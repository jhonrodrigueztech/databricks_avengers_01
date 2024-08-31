# Databricks notebook source
pip install datacontract-cli[deltalake]

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from datacontract.data_contract import DataContract
import os
import re

# COMMAND ----------

fullPath = "/Workspace/Shared/workflows/taller_data_contract/table1_contract.yml"

# COMMAND ----------

data_contract = DataContract(data_contract_file=fullPath)
sql_ddl = data_contract.export(export_format="sql")

regex = """(?<=REPLACE TABLE)(.*?)(?=\()"""
m = re.search(regex, sql_ddl)
table_name = m.group()
  
if spark.catalog.tableExists(table_name): 
    print(f"{table_name} already is in our catalog")
else:
    spark.sql(sql_ddl)
    print(f"{table_name} has been created") 


# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dtw_avengers_lakehouse.avengers_0508.tb_doctor_doom_contract

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load data dummy

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

from pyspark.sql.functions import *


# COMMAND ----------

def casting_columns(df) :
    return (df.withColumn("processing_timestamp", col("processing_timestamp").cast("timestamp"))
                .withColumn("last_sale_timestamp", col("last_sale_timestamp").cast("timestamp"))
                .withColumn("p_auditDate", col("p_auditDate").cast("date"))
                )

# COMMAND ----------

def changeDateByNewValue(df) :
    return df.withColumn("quantity" , col("quantity") * 100)

# COMMAND ----------


simpleData = (
    ("1234567890123", 5, "2024-02-25T16:16:30.171798", "2024-03-25T16:16:30.171807", "2024-02-25"),
    ("1234567890126", 5, "2024-02-25T16:16:30.171798", "2024-03-25T16:16:30.171807", "2024-02-25"),
    ("1234567890124",7, "2024-02-25T16:16:30.171798", "2024-03-25T16:16:30.171807", "2024-02-25")
  )

columns= ["sku", "quantity", "last_sale_timestamp", "processing_timestamp", "p_auditDate"]

dataFrame =  (spark.createDataFrame(data = simpleData, schema = columns)
                .transform(casting_columns)
                .transform(changeDateByNewValue)
                )
                

display(dataFrame)


# COMMAND ----------

dataFrame.write.mode("overwrite").saveAsTable("dtw_avengers_lakehouse.avengers_0508.tb_doctor_doom_contract")

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Validando data Quality

# COMMAND ----------

from datacontract.data_contract import DataContract
import os
import re

# COMMAND ----------

from databricks.connect import DatabricksSession
DatabricksSession.builder.getOrCreate()

# COMMAND ----------

fullPath = "/Workspace/Shared/workflows/taller_data_contract/table1_contract.yml"

import sys

data_contract = DataContract(
    data_contract_file=fullPath , spark=DatabricksSession.builder.getOrCreate()
)

run = data_contract.test()

# COMMAND ----------

print("Data Contract test result:", run.result)

# COMMAND ----------

print("Run details:",  run)

