from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, regexp_extract


if __name__ == '__main__':
    # create spark session
    spark = SparkSession.builder.appName("WikiExtractor").config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.15.0").getOrCreate()
    # read wiki dump file into dataframe
    path = "enwiki-latest-pages-articles.xml.bz2"
    df = spark.read.format("com.databricks.spark.xml").option("rowTag", "page").load(path)
    # select only pages with football in text, birth_place, birth_date and without death_date
    df = df.withColumn('bool', col('revision.text._VALUE').contains('football') & col('revision.text._VALUE').contains('| birth_place') & col('revision.text._VALUE').contains('| birth_date') & ~col('revision.text._VALUE').contains('| death_date'))
    # filter only pages with football in text, birth_place, birth_date and without death_date
    df = df.filter(col('bool') == 'True')
    # drop all columns except title and revision
    df = df.select('title', 'revision')
    # extract birth_place, name and birth_date from text
    df = df.withColumn('birth_place', regexp_extract(col('revision.text._VALUE'), '\| birth_place\s+=(.*)\n', 1))
    df = df.withColumn('name', regexp_extract(col('revision.text._VALUE'), '\| name\s+=(.*)\n', 1))
    df = df.withColumn('birth_date', regexp_extract(col('revision.text._VALUE'), '\| birth_date\s+=(.*)\n', 1))
    # drop all columns except title, name, birth_place and birth_date
    df = df.select('title', 'name', 'birth_place', 'birth_date')
    # save dataframe as tsv file
    df.toPandas().to_csv('output_wiki.tsv', sep='\t', index=False, encoding='utf-8', header=['title', 'name', 'birth_place', 'birth_date'])
    # stop spark session
    spark.stop()