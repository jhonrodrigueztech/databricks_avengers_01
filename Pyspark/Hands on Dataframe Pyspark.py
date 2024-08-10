# Databricks notebook source
simpleData = (
    ("James", "Sales", "3000"), \
    ("Robert", "Sales", "4100"),   \
    ("Jeff", None, "3000"), \
    ("Kumar", None, "200"),\
    ("Saif", "Sales", "4100") \
  )

columns = ["names", "department", "salary"   ]

dataframe = spark.createDataFrame( data = simpleData , schema =  columns  )

dataframe.printSchema()




# COMMAND ----------

display(dataframe)

# COMMAND ----------

from pyspark.sql.functions import *

dfNuevo = (
        dataframe
            .select( "names" , "department", "salary" )
            # .where( col("department") == "Sales" )
            .withColumn("department" , coalesce( col("department") , lit("Tech") )  )
            .withColumn("nueva_column" ,lit( "Default"))
            .withColumn("increase_salary" ,
                        when ( col("department") == "Tech"  , col ("salary") * 0.15  )
                         .when ( col("department") == "RRHH"  , col ("salary") * 0.12  )
                         . when ( col("department") == "Business"  , col ("salary") * 0.08  )
                            .otherwise(lit(0))
                         )
#  col("department") == "Tech" col ("salary ") * 0.15
        )

display(dfNuevo)

# COMMAND ----------

nombre = "Kelly"
mensaje = f"Hola {nombre}"

print(mensaje)

# COMMAND ----------

dfsql = spark.sql(
    f"""
    SELECT names , 
    coalesce(department, 'Tech') as department , 
    salary ,
    case when  department = 'Tech'
      THEN salary * 0.15
      ELSE 0
    END increase_salary,
    'Default' as new_column
    FROM {{df}}
    -- where department = 'Sales'
    """ , df = dataframe
)


display(dfsql)

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

simpleData = (("James", "Sales", 3000), \
    ("Michael", "Sales", 4600),  \
    ("Robert", "Sales", 4100),   \
    ("Maria", "Finance", 3000),  \
    ("James", "Sales", 3000),    \
    ("Scott", "Finance", 3300),  \
    ("Jen", "Finance", 3900),    \
    ("Jeff", "Marketing", 3000), \
    ("Kumar", "Marketing", 2000),\
    ("Saif", "Sales", 4100) \
  )

columns= ["employee_name", "department", "salary"]

dataFrameGroupBy =  spark.createDataFrame(data = simpleData, schema = columns)

dataFrameGroupBy.printSchema()

display(dataFrameGroupBy)


# COMMAND ----------

dfUniques =  dataFrameGroupBy.distinct()

display(dfUniques)

# COMMAND ----------

dfUniques =  dataFrameGroupBy.dropDuplicates(["department"])

display(dfUniques)

# COMMAND ----------

def deleteDuplicatesBySalary (df) :

    from pyspark.sql.window import Window

    windowSpec =  Window.partitionBy("department").orderBy(col("salary").desc())

    return ( df.withColumn("rankeo" , row_number().over(windowSpec) )
               .where("rankeo  == 1")
               .drop("rankeo")
                    )



# COMMAND ----------

dfUsingMethodPython = dataFrameGroupBy.transform(deleteDuplicatesBySalary)

display(dfUsingMethodPython)

# COMMAND ----------



# COMMAND ----------

# from pyspark.sql.window import Window

# windowSpec =  Window.partitionBy("department").orderBy(col("salary").desc())

# dfUniques = ( dataFrameGroupBy
#                 .withColumn("rankeo" , row_number().over(windowSpec) )
#                 .where("rankeo  == 1")
#                 .drop("rankeo")
#                 )
                
# display(dfUniques)

# COMMAND ----------



# COMMAND ----------

dfFinal = (
            dataFrameGroupBy.groupBy("department")
                        .agg( 
                            sum("salary").alias("total_salary"),
                            count("*") ,
                            collect_list("employee_name").alias("empleados")  )
)
display(dfFinal)

# COMMAND ----------

dfSQL = spark.sql(
f"""
    SELECT department, sum(salary) as total_salary ,
    count("*") as counts ,
    collect_list("employee_name") as empleados
    FROM {{df}}
    GROUP BY ALL
""", df = dataFrameGroupBy
    
)

display(dfSQL)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Functions UDF

# COMMAND ----------

from pyspark.sql.functions import *

display(dataframe)


# COMMAND ----------

@udf('string')
def concatenarColumns (n , d) :
    return f" Nombre {n} trabaje en {d} "

@udf('double')
def multiplicarx2 (s) :
    return 2.9

# COMMAND ----------



dfUDF =( dataframe
        .withColumn("udfFunction" , concatenarColumns(col("names") ,col("department")) )
        .withColumn("udfFunction2" , multiplicarx2("salary") ))

display(dfUDF)

# COMMAND ----------


