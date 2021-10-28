# script to make a table w correct schema in postgresql database

# importing columns as strings -> further parse datatype downstream in ETL pipelines
create_table_query = "CREATE UNLOGGED TABLE IF NOT EXISTS rawParcelTable ( \
    ain VARCHAR(15) PRIMARY KEY, \
    situszip VARCHAR(20), \
    rollyear VARCHAR(5) NOT NULL, \
    usecodedescchar1 VARCHAR(20) NOT NULL,\
    sqftmain VARCHAR(10), \
    roll_landvalue VARCHAR(20) NOT NULL, \
    roll_landbaseyear VARCHAR(4) NOT NULL, \
    istaxableparcel VARCHAR(1), \
    center_lat VARCHAR(25), \
    center_lon VARCHAR(25) \
)"
