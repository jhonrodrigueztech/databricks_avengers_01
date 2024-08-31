-- Databricks notebook source


-- COMMAND ----------

CREATE WIDGET TEXT catalog_v2 DEFAULT "students";

-- COMMAND ----------

select  * from  ${catalog_v2}.avengers_0508.students;

-- COMMAND ----------

select  * from  ${catalog_v2}.avengers_0508.students;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.notebook.exit(1)

-- COMMAND ----------

select  * from  ${catalog_v2}.avengers_0508.students;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.notebook.exit(2)

-- COMMAND ----------

select  * from  ${catalog_v2}.avengers_0508.students;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.notebook.exit(0)
