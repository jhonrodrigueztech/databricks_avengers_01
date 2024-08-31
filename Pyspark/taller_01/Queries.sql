-- Databricks notebook source
CREATE OR REPLACE FUNCTION dtw_avengers_lakehouse.silver_dev.decrypt_data (value_cypher STRING, cypher_key STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$ 
  from cryptography.fernet import Fernet

  fernet = Fernet(cypher_key)

  value2 = fernet.decrypt(value_cypher.encode()).decode()

  return value2
$$

-- COMMAND ----------

DECLARE KEY_ = "95oBoGsSAkJNlCd5quoZvZCdTjAVORFUGDhLk2cSNXU=";


-- COMMAND ----------


select *
from dtw_avengers_lakehouse.silver_dev.main_accounts

-- COMMAND ----------


select 
  dtw_avengers_lakehouse.silver_dev.decrypt_data( dni  , KEY_ ) as dni  ,
    dtw_avengers_lakehouse.silver_dev.decrypt_data( fullName  , KEY_ ) as fullName  ,
      dtw_avengers_lakehouse.silver_dev.decrypt_data( email  , KEY_ ) as email  ,
      audit_time
from dtw_avengers_lakehouse.silver_dev.main_accounts
