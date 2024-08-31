-- Databricks notebook source
create or replace table  dtw_avengers_lakehouse.bronze_dev.vehicles_from_mainstreet (id string ,driver string, color string , count_passenger int , ts_auto timestamp);


-- COMMAND ----------

truncate table dtw_avengers_lakehouse.bronze_dev.vehicles_from_mainstreet 

-- COMMAND ----------

INSERT INTO dtw_avengers_lakehouse.bronze_dev.vehicles_from_mainstreet  VALUES ('DMP-9', "Driver 9 Company H" , "white black" , 7 , current_timestamp())
