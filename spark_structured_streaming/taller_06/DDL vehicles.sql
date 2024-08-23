-- Databricks notebook source
select * from dtw_avengers_lakehouse.bronze_dev.vehicles_bronze

-- COMMAND ----------

create or replace table  dtw_avengers_lakehouse.bronze_dev.vehicles_bronze (id string ,driver string, color string , count_passenger int , ts_auto timestamp);


-- COMMAND ----------

INSERT INTO  dtw_avengers_lakehouse.bronze_dev.vehicles_bronze VALUES ('DMP-3', "New Driver INN" , "red" , 7 , current_timestamp())

-- COMMAND ----------


