-- Databricks notebook source
-- MAGIC %python
-- MAGIC import time
-- MAGIC time.sleep(20)

-- COMMAND ----------

CREATE WIDGET TEXT catalog_v2 DEFAULT "students";

select * from ${catalog_v2}.bronze_dev.account_mongodb;


-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.notebook.exit(0)
