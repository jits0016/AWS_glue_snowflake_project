from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
import re
spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
data=r"E:\Bigdata\dataset\world_bank.json"
df=spark.read.format("json").load(data)
#df.printSchema()
res=df.withColumn('theme1name',col('theme1.Name')).withColumn('theme1percent',col('theme1.Percent'))\
    .withColumn('theme_namecode',explode(col('theme_namecode'))).\
    withColumn('theme_code',col('theme_namecode.code'))\
    .withColumn('theme_name',col('theme_namecode.name')).drop('theme_namecode','theme1')
final=res.select('theme1name','theme1percent','theme_name')
output_path=r"F:\aws_project_1"
final.write.mode('overwrite').format('csv').option('header','false').save(output_path)
final.show()
