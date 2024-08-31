# Databricks notebook source
def saveCollectionToLakehouse(database, collection ):

    table = f"dtw_avengers_lakehouse.mongodb.{collection}"

    password = "30A06tuwCe59tMVo"

    dfMongodb = (spark.read
                            .format("com.mongodb.spark.sql.DefaultSource")
                            .option("uri", f"mongodb+srv://teamofsolution:{password}@techengineers.gzrafk4.mongodb.net/?retryWrites=true&w=majority&appName=techEngineers")
                            .option("database", database)
                            .option("collection", collection)
                            .load()
                    )

    dfMongodb.write.format("delta").mode("overwrite").saveAsTable(table)



# COMMAND ----------

loading_tables = [
    ("avengexrs", "accounts"),
    ("edgar_cusi", "test_kafka_from_databricks"),
    ("datapath08", "tb_rows_uniques" ),
    ("datapath", "GabrielDuarteLuna" ),
    ("datapath", "JuanCarlosMamanidelaCruz" ),
    ("datapath", "Manuel_Coaguila_Cornejo_mongo" ),
    ("datapath", "taller_jose_mejia_aprobados" ),
    ("datapath", "tb_notas_alumnos" ),
    ("datapath", "tb_notas_alumnos_romario" ),
    ("datapath08", "michael_hidalgo_cloudatatest" )
]
#2:20



for row in loading_tables:
    database = row[0]
    collection = row[1]
    try:
        saveCollectionToLakehouse( database, collection  )

        print(f"Database {database} with table {collection} was created")
    except:
        print(f"Table {collection} hasn't created")



# COMMAND ----------

def saveCollectionToLakehouseExecutor(row ):

    database = row[0]
    collection = row[1]

    table = f"dtw_avengers_lakehouse.mongodb.{collection}"

    password = "30A06tuwCe59tMVo"

    dfMongodb = (spark.read
                            .format("com.mongodb.spark.sql.DefaultSource")
                            .option("uri", f"mongodb+srv://teamofsolution:{password}@techengineers.gzrafk4.mongodb.net/?retryWrites=true&w=majority&appName=techEngineers")
                            .option("database", database)
                            .option("collection", collection)
                            .load()
                    )

    message = ""

    try:
        dfMongodb.write.format("delta").mode("overwrite").saveAsTable(table)
        message = f"Database {database} with table {collection} was created"
    except:
        message = f"Database {database} with table {collection} was failed"

    return  message



# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended  dtw_avengers_lakehouse.avengers_0508.students

# COMMAND ----------

loading_tables = [
    ("avengexrs", "accounts"),
    ("edgar_cusi", "test_kafka_from_databricks"),
    ("datapath08", "tb_rows_uniques" ),
    ("datapath", "GabrielDuarteLuna" ),
    ("datapath", "JuanCarlosMamanidelaCruz" ),
    ("datapath", "Manuel_Coaguila_Cornejo_mongo" ),
    ("datapath", "taller_jose_mejia_aprobados" ),
    ("datapath", "tb_notas_alumnos" ),
    ("datapath", "tb_notas_alumnos_romario" ),
    ("datapath08", "michael_hidalgo_cloudatatest" )
]
#2:20

# 18 seg

import concurrent.futures

with concurrent.futures.ThreadPoolExecutor() as executor:
    
    futures = [executor.submit(saveCollectionToLakehouseExecutor, i) for i in loading_tables]

    results = [future.result() for future in concurrent.futures.as_completed(futures)]


for r in results:

    print(r)


# COMMAND ----------


