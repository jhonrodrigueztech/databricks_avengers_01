-- Databricks notebook source
create  or replace table dtw_avengers_lakehouse.bronze_dev.pasajeros (idcar string , passenger string, platform string, dni string, ts_message timestamp)

-- COMMAND ----------

select * from dtw_avengers_lakehouse.bronze_dev.pasajeros

-- COMMAND ----------

INSERT INTO dtw_avengers_lakehouse.bronze_dev.pasajeros  VALUES ('DMP-3', "New Passenger 9" , "fb" , "16855" , current_timestamp()) 
