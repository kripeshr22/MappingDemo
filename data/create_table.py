# script to make a table w correct schema in postgresql database
# database name is "parcelDatabase"
fields = [
    'situszip',
    'ain',
    'rollyear',
    'usecodedescchar1',  # general use type: residential or commercial
    'sqftmain',
    'roll_landvalue',
    'roll_landbaseyear',
    'roll_impvalue',
    'roll_impbaseyear',
    'roll_totlandimp',
    'istaxableparcel',
    'roll_totalvalue',
    'nettaxablevalue',
    'rowid',
    'center_lat',
    'center_lon',
]

# importing columns as strings -> further parse datatype downstream in ETL pipelines
create_table_query = "CREATE TABLE IF NOT EXISTS rawParcelTable ( \
    situszip VARCHAR(20), \
    ain VARCHAR(15) NOT NULL, \
    rollyear VARCHAR(4), \
    usecodedescchar1 VARCHAR(20), \
    sqftmain VARCHAR(10), \
    roll_landvalue VARCHAR(20) NOT NULL, \
    roll_landbaseyear VARCHAR(4) NOT NULL, \
    roll_impvalue VARCHAR(20) NOT NULL, \
    roll_impbaseyear VARCHAR(4) NOT NULL, \
    roll_totlandimp VARCHAR(20) NOT NULL, \
    istaxableparcel VARCHAR(1) NOT NULL, \
    roll_totalvalue VARCHAR(20) NOT NULL, \
    nettaxablevalue VARCHAR(20) NOT NULL, \
    rowid VARCHAR(15) PRIMARY KEY, \
    center_lat VARCHAR(25), \
    center_lon VARCHAR(25) \
)"
