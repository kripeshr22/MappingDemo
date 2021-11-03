# script to make a table w correct schema in postgresql database

# importing columns as strings -> further parse datatype downstream in ETL pipelines
create_table_query_1 = "CREATE UNLOGGED TABLE IF NOT EXISTS svr_table_1 ( \
    ain VARCHAR(15) PRIMARY KEY, \
    situszip VARCHAR(20) NOT NULL, \
    usecodedescchar1 VARCHAR(20) NOT NULL,\
    sqftmain VARCHAR(10), \
    roll_landvalue VARCHAR(20) NOT NULL, \
    roll_landbaseyear VARCHAR(4) NOT NULL, \
    istaxableparcel VARCHAR(1), \
    center_lat VARCHAR(25) NOT NULL, \
    center_lon VARCHAR(25) NOT NULL \
)"

create_table_query_2 = "CREATE UNLOGGED TABLE IF NOT EXISTS svr_table_2 ( \
    ain VARCHAR(15) PRIMARY KEY, \
    taxratearea VARCHAR(5) NOT NULL, \
    usecode VARCHAR(5) NOT NULL, \
    usecodedescchar1 VARCHAR(20) NOT NULL,\
    usecodedescchar2 VARCHAR(100), \
    yearbuilt VARCHAR(4) NOT NULL,     \
    effectiveyearbuilt VARCHAR(4) NOT NULL,     \
    sqftmain VARCHAR(10) NOT NULL, \
    roll_landvalue VARCHAR(20) NOT NULL, \
    roll_landbaseyear VARCHAR(4) NOT NULL, \
    istaxableparcel VARCHAR(1) NOT NULL, \
    cluster VARCHAR(5) NOT NULL, \
    situszip5 VARCHAR(5) NOT NULL, \
    center_lat VARCHAR(25) NOT NULL, \
    center_lon VARCHAR(25) NOT NULL \
)"



fields_2 = [
    'ain',
    # 'situszip',
    # 'taxratearea_city',
    # 'rollyear',
    'taxratearea',
    # 'assessorid',
    # 'propertylocation',
    # 'usetype',
    'usecode',  # property use type encoded as number
    'usecodedescchar1',  # general use type: residential or commercial
    'usecodedescchar2',  # i.e. office, store, etc.
    # 'usecodedescchar3',
    # 'usecodedescchar4',
    # 'totbuildingdatalines',
    'yearbuilt',
    'effectiveyearbuilt',
    'sqftmain',
    # 'bedrooms',
    # 'bathrooms',
    # 'units',
    # 'recordingdate',
    'roll_landvalue',
    'roll_landbaseyear',  # this gets updated when change in ownership
    # 'roll_impvalue',
    # 'roll_impbaseyear',
    # 'roll_totlandimp',
    # 'roll_homeownersexemp',
    # 'roll_realestateexemp',
    # 'roll_fixturevalue',
    # 'roll_fixtureexemp',
    # 'roll_perspropvalue',
    # 'roll_perspropexemp',
    'istaxableparcel',
    # 'roll_totalvalue',
    # 'roll_totalexemption',
    # 'nettaxablevalue',
    # 'parcelclassification',
    # 'adminregion',
    'cluster',  # geographical area by which similar types of parcels are grouped
    # 'parcelboundarydescription',
    # 'situshouseno',
    # 'situsfraction',
    # 'situsdirection',
    # 'situsstreet',
    # 'situsunit',
    # 'situscity',
    'situszip5',
    # 'rowid',
    'center_lat',
    'center_lon',
    # 'location_1',
]


# all columns
fields_1 = [
    'ain',
    'situszip',
    # 'taxratearea_city',
    # 'rollyear',
    # 'taxratearea',
    # 'assessorid',
    # 'propertylocation',
    # 'usetype',
    # 'usecode',
    'usecodedescchar1',  # general use type: residential or commercial
    # 'usecodedescchar2',
    # 'usecodedescchar3',
    # 'usecodedescchar4',
    # 'totbuildingdatalines',
    # 'yearbuilt',
    # 'effectiveyearbuilt',
    'sqftmain',
    # 'bedrooms',
    # 'bathrooms',
    # 'units',
    # 'recordingdate',
    'roll_landvalue',
    'roll_landbaseyear',  # this gets updated when change in ownership
    # 'roll_impvalue',
    # 'roll_impbaseyear',
    # 'roll_totlandimp',
    # 'roll_homeownersexemp',
    # 'roll_realestateexemp',
    # 'roll_fixturevalue',
    # 'roll_fixtureexemp',
    # 'roll_perspropvalue',
    # 'roll_perspropexemp',
    'istaxableparcel',
    # 'roll_totalvalue',
    # 'roll_totalexemption',
    # 'nettaxablevalue',
    # 'parcelclassification',
    # 'adminregion',
    # 'cluster',
    # 'parcelboundarydescription',
    # 'situshouseno',
    # 'situsfraction',
    # 'situsdirection',
    # 'situsstreet',
    # 'situsunit',
    # 'situscity',
    # 'situszip5',
    # 'rowid',
    'center_lat',
    'center_lon',
    # 'location_1',
]
