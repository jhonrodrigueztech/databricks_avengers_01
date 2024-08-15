# Databricks notebook source
notebook_path = dbutils.widgets.get("notebook_path")
catalog_ = dbutils.widgets.get("catalog")

result = dbutils.notebook.run( notebook_path, 60000000 , { "catalog_v2": catalog_ }   )

# COMMAND ----------

dbutils.jobs.taskValues.set(key="result" , value=result)

# COMMAND ----------

# MAGIC %sql
# MAGIC alter table add column ("")

# COMMAND ----------

df = spark.sql("describe history dtw_avengers_lakehouse.avengers_0508.personas")

display(df)

# COMMAND ----------

# MAGIC %sql
# MAGIC restore table add column ("")
