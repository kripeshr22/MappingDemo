# script to make a table w correct schema in postgresql database

# importing columns as strings -> further parse datatype downstream in ETL pipelines

# remove last location value because redundant and dictionary type value requires extra parsing step
raw_socrata_table_schema = "CREATE UNLOGGED TABLE IF NOT EXISTS rawLACountyTable ( \
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
        rowID VARCHAR PRIMARY KEY, \
        CENTER_LAT VARCHAR, \
        CENTER_LON VARCHAR \
)"

raw_csv_table_schema = "CREATE UNLOGGED TABLE IF NOT EXISTS rawLACountyTable ( \
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
        rowID VARCHAR PRIMARY KEY, \
        CENTER_LAT VARCHAR, \
        CENTER_LON VARCHAR, \
        Location VARCHAR \
)"


# for csv imports only
all_fields_csv = [
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


# for API imports only
all_fields_socrata = [
    'situszip',
    'taxratearea_city',
    'ain',
    'rollyear',
    'taxratearea',
    'assessorid',
    'propertylocation',
    'usetype',
    'usecode',  # property use type encoded as number
    'usecodedescchar1',  # general use type: residential or commercial
    'usecodedescchar2',  # i.e. office, store, etc.
    'usecodedescchar3',
    'usecodedescchar4',
    'totbuildingdatalines',
    'yearbuilt',
    'effectiveyearbuilt',
    'sqftmain',
    'bedrooms',
    'bathrooms',
    'units',
    'recordingdate',
    'roll_landvalue',
    'roll_landbaseyear',  # this gets updated when change in ownership
    'roll_impvalue',
    'roll_impbaseyear',
    'roll_totlandimp',
    'roll_homeownersexemp',
    'roll_realestateexemp',
    'roll_fixturevalue',
    'roll_fixtureexemp',
    'roll_perspropvalue',
    'roll_perspropexemp',
    'istaxableparcel',
    'roll_totalvalue',
    'roll_totalexemption',
    'nettaxablevalue',
    'parcelclassification',
    'adminregion',
    'cluster',  # geographical area by which similar types of parcels are grouped
    'parcelboundarydescription',
    'situshouseno',
    'situsfraction',
    'situsdirection',
    'situsstreet',
    'situsunit',
    'situscity',
    'situszip5',
    'rowid',
    'center_lat',
    'center_lon',
    # 'location_1',
]

