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

create_raw_table = "CREATE UNLOGGED TABLE IF NOT EXISTS rawLACountyTable ( \
        ZIPcode VARCHAR(10), \
        TaxRateArea_CITY VARCHAR(50), \
        AIN VARCHAR(15), \
        RollYear VARCHAR(4), \
        TaxRateArea VARCHAR(10), \
        AssessorID VARCHAR(20), \
        PropertyLocation VARCHAR(50), \
        PropertyType VARCHAR(100), \
        PropertyUseCode VARCHAR(4), \
        GeneralUseType VARCHAR(20), \
        SpecificUseType VARCHAR(100), \
        SpecificUseDetail1 VARCHAR(100), \
        SpecificUseDetail2 VARCHAR(100), \
        totBuildingDataLines VARCHAR(10), \
        YearBuilt VARCHAR(4), \
        EffectiveYearBuilt VARCHAR(4), \
        SQFTmain VARCHAR(10), \
        Bedrooms VARCHAR(3), \
        Bathrooms VARCHAR(3), \
        Units VARCHAR(5), \
        RecordingDate VARCHAR(20), \
        LandValue VARCHAR(20), \
        LandBaseYear VARCHAR(4), \
        ImprovementValue VARCHAR(10), \
        ImpBaseYear VARCHAR(4), \
        TotalLandImpValue VARCHAR(20), \
        HomeownersExemption VARCHAR(10), \
        RealEstateExemption VARCHAR(10), \
        FixtureValue VARCHAR(10), \
        FixtureExemption VARCHAR(10), \
        PersonalPropertyValue VARCHAR(10), \
        PersonalPropertyExemption VARCHAR(10), \
        isTaxableParcel VARCHAR(10), \
        TotalValue VARCHAR(20), \
        TotalExemption VARCHAR(20), \
        netTaxableValue VARCHAR(20), \
        SpecialParcelClassification VARCHAR(20), \
        AdministrativeRegion VARCHAR(4), \
        Cluster VARCHAR(10), \
        ParcelBoundaryDescription VARCHAR(200), \
        HouseNo VARCHAR(10), \
        HouseFraction VARCHAR(10), \
        StreetDirection VARCHAR(10), \
        StreetName VARCHAR(50), \
        UnitNo VARCHAR(10), \
        City VARCHAR(50), \
        ZIPcode5 VARCHAR(5), \
        rowID VARCHAR(20), \
        CENTER_LAT VARCHAR(25), \
        CENTER_LON VARCHAR(25), \
        Location VARCHAR(100) \
)"


csv_fields = [
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
