# Databricks notebook source
# MAGIC %sql
# MAGIC select * from dtw_avengers_lakehouse.bronze_dev.account_mongodb

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dtw_avengers_lakehouse.bronze_dev.account_mongodb

# COMMAND ----------

dfAccountsBronze = spark.table("dtw_avengers_lakehouse.bronze_dev.account_mongodb")

# COMMAND ----------

from cryptography.fernet import Fernet

key = "95oBoGsSAkJNlCd5quoZvZCdTjAVORFUGDhLk2cSNXU="

@udf('string')
def decrypt(value_cypher , key):
    fernet = Fernet(key)
    #  AES256 PADDING
    value = fernet.decrypt(value_cypher.encode()).decode()

    return value

# COMMAND ----------

# MAGIC %sql
# MAGIC truncate table dtw_avengers_lakehouse.silver_dev.main_accounts

# COMMAND ----------

def deleteDuplicatesBySalary (df) :

    from pyspark.sql.window import Window

    windowSpec =  Window.partitionBy("dni").orderBy(col("arrive_date").desc())

    return ( df.withColumn("rankeo" , row_number().over(windowSpec) )
               .where("rankeo  == 1")
               .drop("rankeo")
                    )



# COMMAND ----------

from pyspark.sql.functions import *

dfBronzeDecryptRowUniques = (dfAccountsBronze
                .select(
                    decrypt(col("dni") , lit(key)).alias("dni"), 
                    decrypt(col("email") ,  lit(key)).alias("email"), 
                    decrypt(col("fullName") ,  lit(key)).alias("fullName"), 
                    col("arrive_date") , 
                    current_timestamp().alias("audit_time"))
                .transform(deleteDuplicatesBySalary) 
                )
                
dfFinal = spark.sql(
 f"""
    MERGE WITH SCHEMA EVOLUTION INTO dtw_avengers_lakehouse.silver_dev.main_accounts m
    USING {{df}} inn
    ON m.dni = inn.dni
    WHEN MATCHED 
    THEN UPDATE SET *
    WHEN NOT MATCHED 
    THEN INSERT *
""" , df = dfBronzeDecryptRowUniques
)                    


# COMMAND ----------

display(dfFinal)

# COMMAND ----------

display(dfFinal)

# COMMAND ----------

@udf('string')
def encrypt(value , key):
    fernet = Fernet(key)

    value_bites = bytes(value , 'utf-8')

    cypher_value = fernet.encrypt(value_bites)

    cypher_decode = str(  cypher_value.decode('ascii')   )

    return cypher_decode

# COMMAND ----------

key = "95oBoGsSAkJNlCd5quoZvZCdTjAVORFUGDhLk2cSNXU="

dfEncrypt = (spark.table("dtw_avengers_lakehouse.silver_dev.main_accounts")
        .withColumn("dni", encrypt(col("dni"), lit(key)))
        .withColumn("email", encrypt(col("email"), lit(key)))
        .withColumn("fullName", encrypt(col("fullName"), lit(key)))
)


dfEncrypt.write.format("delta").mode("overwrite").saveAsTable("dtw_avengers_lakehouse.silver_dev.main_accounts")

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dtw_avengers_lakehouse.silver_dev.main_accounts
