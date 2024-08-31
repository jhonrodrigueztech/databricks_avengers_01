-- Databricks notebook source
truncate table dtw_avengers_lakehouse.bronze_dev.vehicles_bronze

-- COMMAND ----------

select * from dtw_avengers_lakehouse.bronze_dev.vehicles_bronze

-- COMMAND ----------

create or replace table  dtw_avengers_lakehouse.bronze_dev.vehicles_bronze (id string ,driver string, color string , count_passenger int , ts_auto timestamp);


-- COMMAND ----------

INSERT INTO  dtw_avengers_lakehouse.bronze_dev.vehicles_bronze VALUES ('DMP-3', "Driver 3" , "white" , 7 , current_timestamp())

-- COMMAND ----------


