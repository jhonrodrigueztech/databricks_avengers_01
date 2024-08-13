# Databricks notebook source
# mongodb :: org.mongodb.spark:mongo-spark-connector_2.12:3.0.2
# 

password = "30A06tuwCe59tMVo"

dfMongoDBAccounts = (spark.read
                        .format("com.mongodb.spark.sql.DefaultSource")
                        .option("uri", f"mongodb+srv://teamofsolution:{password}@techengineers.gzrafk4.mongodb.net/?retryWrites=true&w=majority&appName=techEngineers")
                        .option("database", "avengers")
                        .option("collection", "accounts")
                        .load()
                   )

display(dfMongoDBAccounts)


# COMMAND ----------

# MAGIC %md
# MAGIC ## Fernet Library Cypher Decryp - Decrypt
# MAGIC

# COMMAND ----------

from cryptography.fernet import Fernet

key = Fernet.generate_key()

print(key)

# COMMAND ----------

f = Fernet(key)
print(f.encrypt(b"Jhon Rodriguez"))

# COMMAND ----------

print(f.decrypt("gAAAAABmtssdyIvYdWvoOMS4aj68NF-xESVQRTt1YfYzI3httnk7IFgaVzCkmGFnTkOl4Y87EKlxWYRQYlGL6aJAhwiVuKSUHw=="))

# COMMAND ----------

@udf('string')
def encrypt(value , key):
    fernet = Fernet(key)

    value_bites = bytes(value , 'utf-8')

    cypher_value = fernet.encrypt(value_bites)

    cypher_decode = str(  cypher_value.decode('ascii')   )

    return cypher_decode

# COMMAND ----------

from pyspark.sql.functions import *


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE dtw_avengers_lakehouse.bronze_dev.account_mongodb (
# MAGIC id String,
# MAGIC dni STRING,
# MAGIC email STRING,
# MAGIC fullName STRING,
# MAGIC cardNumber STRING,
# MAGIC arrive_date DATE,
# MAGIC processing_time TIMESTAMP GENERATED ALWAYS AS (now())
# MAGIC )

# COMMAND ----------

from cryptography.fernet import Fernet

key = "95oBoGsSAkJNlCd5quoZvZCdTjAVORFUGDhLk2cSNXU="

dfCypher = (
        dfMongoDBAccounts.withColumn("cardNumber" , encrypt("cardNumber" , lit(key)) )
            .withColumn("dni" , encrypt("dni" , lit(key)) )
            .withColumn("email" , encrypt("email" , lit(key)) )
            .withColumn("fullName" , encrypt("fullName" , lit(key)) )
            .withColumn("arrive_date" , coalesce(
                                        col("arrive_date") , 
                                        lit("2024-08-09")).cast("date") )
            .withColumn("id" , col("_id.oid"))
            .drop("_id")
            )

dfCypher.write.format("delta").mode("append").saveAsTable("dtw_avengers_lakehouse.bronze_dev.account_mongodb")



# COMMAND ----------

# MAGIC %md
# MAGIC ## CONNECT SPARK WITH CONFLUENT KAFKA

# COMMAND ----------

# org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3
key = "X4TCJ75W3DAP5KHJ"
secret = "gaAKphXY6BjGRi53T9qsvCEvku5X06S2AkvRLiaHpYWZnGrMSbdE7vYC0llo96rR"
server = "pkc-6vz38.westus2.azure.confluent.cloud:9092"

dfFromKafka = (
            spark.read.format("kafka")
                .option("subscribe","topic_doctor_doom")
                .option("kafka.security.protocol", "SASL_SSL") 
                .option("kafka.sasl.jaas.config",
                        f"org.apache.kafka.common.security.plain.PlainLoginModule required username='{key}' password='{secret}';") 
                .option("kafka.sasl.mechanism", "PLAIN") 
                .option("kafka.bootstrap.servers", server) 
                .option("startingOffsets", "earliest") 
                .load()
                .withColumn("id", col("key").cast("string")  )
                .withColumn("value", col("value").cast("string")  )
                 .withColumn("value", parse_json( col("value")) )
                 .withColumn("origen_time" , col("timestamp"))
                 .select("id", "value", "topic", "origen_time")
                )

(dfFromKafka.write
.format("delta")
.mode("append") # overwrite , delete 
.saveAsTable("dtw_avengers_lakehouse.bronze_dev.transactions_kafka"))


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE dtw_avengers_lakehouse.bronze_dev.transactions_kafka(
# MAGIC id String,
# MAGIC value VARIANT,
# MAGIC topic STRING,
# MAGIC origen_time TIMESTAMP,
# MAGIC processing_time TIMESTAMP GENERATED ALWAYS AS (now())
# MAGIC )
# MAGIC
