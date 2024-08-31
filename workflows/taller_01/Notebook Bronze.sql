-- Databricks notebook source
-- MAGIC %python
-- MAGIC import time
-- MAGIC time.sleep(1)

-- COMMAND ----------

CREATE WIDGET TEXT table_v2 DEFAULT "students";

select * from dtw_avengers_lakehouse.avengers_0508.${table_v2};

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.jobs.taskValues.set(key="state", value="succesfull")
