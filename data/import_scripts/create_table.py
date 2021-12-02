# script to make a table w correct schema in postgresql database

# importing columns as strings -> further parse datatype downstream in ETL pipelines
create_test_table = """CREATE UNLOGGED TABLE IF NOT EXISTS testtable (
    ain VARCHAR PRIMARY KEY, \
    situszip VARCHAR, \
    usecodedescchar1 VARCHAR\
)"""

test_fields = ["ain", "situszip", "usecodedescchar1"]
create_table_query_1 = "CREATE UNLOGGED TABLE IF NOT EXISTS svr_table_1 ( \
    ain VARCHAR PRIMARY KEY, \
    situszip VARCHAR, \
    usecodedescchar1 VARCHAR,\
    sqftmain VARCHAR, \
    roll_landvalue VARCHAR, \
    roll_landbaseyear VARCHAR, \
    istaxableparcel VARCHAR, \
    center_lat VARCHAR, \
    center_lon VARCHAR \
)"

create_table_query_2 = "CREATE UNLOGGED TABLE IF NOT EXISTS svr_table_2 ( \
    ain VARCHAR PRIMARY KEY, \
    taxratearea VARCHAR NOT NULL, \
    usecode VARCHAR NOT NULL, \
    usecodedescchar1 VARCHAR NOT NULL,\
    usecodedescchar2 VARCHAR, \
    yearbuilt VARCHAR(4) NOT NULL,     \
    effectiveyearbuilt VARCHAR(4) NOT NULL,     \
    sqftmain VARCHAR NOT NULL, \
    roll_landvalue VARCHAR NOT NULL, \
    roll_landbaseyear VARCHAR(4) NOT NULL, \
    istaxableparcel VARCHAR(1) NOT NULL, \
    cluster VARCHAR NOT NULL, \
    situszip5 VARCHAR(5) NOT NULL, \
    center_lat VARCHAR NOT NULL, \
    center_lon VARCHAR NOT NULL \
)"

create_raw_table = "CREATE UNLOGGED TABLE IF NOT EXISTS rawLACountyTable ( \
        ZIPcode VARCHAR, \
        TaxRateArea_CITY VARCHAR, \
        AIN VARCHAR, \
        RollYear VARCHAR(4), \
        TaxRateArea VARCHAR, \
        AssessorID VARCHAR, \
        PropertyLocation VARCHAR, \
        PropertyType VARCHAR, \
        PropertyUseCode VARCHAR(4), \
        GeneralUseType VARCHAR, \
        SpecificUseType VARCHAR, \
        SpecificUseDetail1 VARCHAR, \
        SpecificUseDetail2 VARCHAR, \
        totBuildingDataLines VARCHAR, \
        YearBuilt VARCHAR(4), \
        EffectiveYearBuilt VARCHAR(4), \
        SQFTmain VARCHAR, \
        Bedrooms VARCHAR, \
        Bathrooms VARCHAR, \
        Units VARCHAR, \
        RecordingDate VARCHAR, \
        LandValue VARCHAR, \
        LandBaseYear VARCHAR, \
        ImprovementValue VARCHAR, \
        ImpBaseYear VARCHAR(4), \
        TotalLandImpValue VARCHAR, \
        HomeownersExemption VARCHAR, \
        RealEstateExemption VARCHAR, \
        FixtureValue VARCHAR, \
        FixtureExemption VARCHAR, \
        PersonalPropertyValue VARCHAR, \
        PersonalPropertyExemption VARCHAR, \
        isTaxableParcel VARCHAR(1), \
        TotalValue VARCHAR, \
        TotalExemption VARCHAR, \
        netTaxableValue VARCHAR, \
        SpecialParcelClassification VARCHAR, \
        AdministrativeRegion VARCHAR(4), \
        Cluster VARCHAR, \
        ParcelBoundaryDescription VARCHAR, \
        HouseNo VARCHAR, \
        HouseFraction VARCHAR, \
        StreetDirection VARCHAR, \
        StreetName VARCHAR, \
        UnitNo VARCHAR, \
        City VARCHAR, \
        ZIPcode5 VARCHAR(5), \
        rowID VARCHAR, \
        CENTER_LAT VARCHAR, \
        CENTER_LON VARCHAR, \
        Location VARCHAR \
)"


all_fields = [
        'ZIPcode',
        'TaxRateArea_CITY',
        'AIN',
        'RollYear',
        'TaxRateArea',
        'AssessorID',
        'PropertyLocation',
        'PropertyType',
        'PropertyUseCode',
        'GeneralUseType',  # general use type: residential or commercial
        'SpecificUseType',
        'SpecificUseDetail1',
        'SpecificUseDetail2',
        'totBuildingDataLines',
        'YearBuilt',
        'EffectiveYearBuilt',
        'SQFTmain',
        'Bedrooms',
        'Bathrooms',
        'Units',
        'RecordingDate',
        'LandValue',
        'LandBaseYear',  # this gets updated when change in ownership
        'ImprovementValue',
        'ImpBaseYear',
        'TotalLandImpValue',
        'HomeownersExemption',
        'RealEstateExemption',
        'FixtureValue',
        'FixtureExemption',
        'PersonalPropertyValue',
        'PersonalPropertyExemption',
        'isTaxableParcel?',
        'TotalValue',
        'TotalExemption',
        'netTaxableValue',
        'SpecialParcelClassification',
        'AdministrativeRegion',
        'Cluster',
        'ParcelBoundaryDescription',
        'HouseNo',
        'HouseFraction',
        'StreetDirection',
        'StreetName',
        'UnitNo',
        'City',
        'ZIPcode5',
        'rowID',
        'CENTER_LAT',
        'CENTER_LON',
        'Location 1',
]



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
