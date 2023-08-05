==================================
# Spark Safe Delta
==================================

Combination of tools that allow more convenient use of PySpark within Azure DataBricks environment.

## Package contents:
=========

    ### 1.delta_write_safe
    -------------
    Tool that allows to automatically update schema of DataBricks Delta in case of Changes in data structure

    ### 1.write_data_mysql
    -------------
    Method writes data into MySQL and takes care of repartitioning in case if it's necessary.

        Dependencies:
          1. MySQL connector Java 8_0_13
          dbfs:/FileStore/jars/7b863f06_67cf_4a51_8f3b_67d414d808b3-Barnymysql_connector_java_8_0_13_4ac45-2f7c7.jar

          http://dev.mysql.com/doc/connector-j/en/
          https://mvnrepository.com/artifact/mysql/mysql-connector-java

        By default, it relies on constant variables outside of method that define MySQL credentials, that can be also specified as a parameters:
            * MYSQL_URL
            * MYSQL_DRIVER
            * MYSQL_USER
            * MYSQL_PASSWORD
            * MYSQL_SSL_CA_PATH
            * MYSQL_QUERY_TIMEOUT

        Method Parameters:
           * p_spark_dataframe - dataframe to write
           * p_mysql_db_name - name of database to write to
           * p_mysql_table_name - name of table to write to
           * p_num_partitions - amount of partitions, if -1, runs with default amount of partitions defined in spark environment or specific delta

       Method default parameters:
            p_num_partitions=-1
            url=MYSQL_URL,
            driver=MYSQL_DRIVER,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            ssl_ca=MYSQL_SSL_CA_PATH,
            queryTimeout=MYSQL_QUERY_TIMEOUT

       Usage example:
          #MySQL settings defined outside of a method below:
          MYSQL_DRIVER = "com.mysql.jdbc.Driver"
          MYSQL_URL = "jdbc:mysql://hostname:port/database?useUnicode=true&characterEncoding=utf-8&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false"
          MYSQL_QUERY_TIMEOUT = 0

          MYSQL_USER = "user@namespace"
          MYSQL_PASSWORD = "example_password"
          MYSQL_SSL_CA_PATH = "/mnt/alex-experiments-blob/certs/cert.txt"

          #Method execution itself
          write_data_mysql(p_spark_dataframe=target_data, p_mysql_dbtable=destination_db_name_column_name_construct)

    ### 3.remove_columns
    -------------
        remove_columns() method removes columns from a specified dataframe.
        It will silently return a result even if user specifies column that doesn't exist.
        Usage example: destination_df = remove_columns(source_df, "SequenceNumber;Body;Non-existng-column")

    ### 4.read_mysql
    -------------
        Method allows fetch the table, or a query as a Spark DataFrame.
        Returnws Spark DataFrame as a result.

        # Example usage:
        read_mysql(table_name=customers)
        read_mysql(table_name=h2.customers)
        read_mysql(table_name=h2.customers, url=MYSQL_URL, driver=MYSQL_DRIVER, user=MYSQL_USER, password=MYSQL_PASSWORD, ssl_ca=MYSQL_SSL_CA_PATH, queryTimeout=MYSQL_QUERY_TIMEOUT)

    ### 4.list_available_mysql_tables
    -------------
        Method allows to list all the tables that available to a particular user.
        Returnws Spark DataFrame as a result


## Package sample usage:
=========
    ``
    #!/usr/bin/env python

    from sparksafedelta import sparksafedelta
    sparksafedelta.delta_write_safe(sp_df_to_write, SP_CONTEXT, DATABRICKS_TABLE_NAME)
    ``