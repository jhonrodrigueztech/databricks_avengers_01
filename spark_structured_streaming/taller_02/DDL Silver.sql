-- Databricks notebook source
describe extended dtw_avengers_lakehouse.silver_dev.accounts_main_silver

-- COMMAND ----------

select * from dtw_avengers_lakehouse.silver_dev.accounts_main_silver

-- COMMAND ----------

create table dtw_avengers_lakehouse.silver_dev.accounts_main_silver (
  dni STRING,
  preferences array<INT>,
  accounts struct <  full_name STRING, phone_number STRING, email STRING , password STRING  > ,
  buckets struct < card_number STRING, type_card STRING , ubication STRING> ,
  settings struct < background STRING, photo STRING, letter_size INT, avatar_name STRING > ,
  processing_time timestamp
)

-- COMMAND ----------

select * from dtw_avengers_lakehouse.bronze_dev.accounts_brz;

-- COMMAND ----------

select * from dtw_avengers_lakehouse.bronze_dev.settings_brz;

-- COMMAND ----------

select * from dtw_avengers_lakehouse.bronze_dev.buckets_brz;
