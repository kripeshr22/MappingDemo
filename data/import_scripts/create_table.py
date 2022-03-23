# script to make a table w correct schema in postgresql database

# importing columns as strings -> further parse datatype downstream in ETL pipelines

# remove last location value because redundant and dictionary type value requires extra parsing step

# some notes on changed vars:
# ain/rowid - cant fit in INT, so I left it as a VARCHAR. it could be a BIGINT (not sure which is better)
# looked into dates - doesnt look like theres a year option so I didn't end up using it (and used ints instead)
# did use date for recording date since in correct format
# money type takes in $1,000.00 type form - used for money stuff

raw_socrata_table_schema_la = "CREATE UNLOGGED TABLE IF NOT EXISTS rawLACountyTable ( \
        ZIPcode INT, \
        TaxRateArea_CITY VARCHAR, \
        AIN VARCHAR, \
        RollYear INT(4), \
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
        YearBuilt INT(4), \
        EffectiveYearBuilt INT(4), \
        SQFTmain INT, \
        Bedrooms VARCHAR, \
        Bathrooms VARCHAR, \
        Units VARCHAR, \
        RecordingDate DATE, \
        LandValue MONEY, \
        LandBaseYear INT, \
        ImprovementValue MONEY, \
        ImpBaseYear INT(4), \
        TotalLandImpValue MONEY, \
        HomeownersExemption MONEY, \
        RealEstateExemption MONEY, \
        FixtureValue MONEY, \
        FixtureExemption MONEY, \
        PersonalPropertyValue MONEY, \
        PersonalPropertyExemption MONEY, \
        isTaxableParcel VARCHAR(1), \
        TotalValue MONEY, \
        TotalExemption MONEY, \
        netTaxableValue MONEY, \
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
        ZIPcode5 INT(5), \
        rowID VARCHAR PRIMARY KEY, \
        CENTER_LAT VARCHAR, \
        CENTER_LON VARCHAR \
)"

raw_csv_table_schema_la = "CREATE UNLOGGED TABLE IF NOT EXISTS rawLACountyTable ( \
        ZIPcode INT, \
        TaxRateArea_CITY VARCHAR, \
        AIN VARCHAR, \
        RollYear INT(4), \
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
        YearBuilt INT(4), \
        EffectiveYearBuilt INT(4), \
        SQFTmain INT, \
        Bedrooms VARCHAR, \
        Bathrooms VARCHAR, \
        Units VARCHAR, \
        RecordingDate DATE, \
        LandValue MONEY, \
        LandBaseYear INT, \
        ImprovementValue MONEY, \
        ImpBaseYear INT(4), \
        TotalLandImpValue MONEY, \
        HomeownersExemption MONEY, \
        RealEstateExemption MONEY, \
        FixtureValue MONEY, \
        FixtureExemption MONEY, \
        PersonalPropertyValue MONEY, \
        PersonalPropertyExemption MONEY, \
        isTaxableParcel VARCHAR(1), \
        TotalValue MONEY, \
        TotalExemption MONEY, \
        netTaxableValue MONEY, \
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
        ZIPcode5 INT(5), \
        rowID VARCHAR PRIMARY KEY, \
        CENTER_LAT VARCHAR, \
        CENTER_LON VARCHAR, \
        Location VARCHAR \
)"


# for csv imports only
all_fields_csv_la = [
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
all_fields_socrata_la = [
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


# script to make a table w correct schema in postgresql database

# importing columns as strings -> further parse datatype downstream in ETL pipelines

raw_socrata_table_schema_sf = "CREATE UNLOGGED TABLE IF NOT EXISTS rawSFCountyTable ( \
        ClosedRollYear INT(4), \
        PropertyLocation VARCHAR, \
        ParcelNumber VARCHAR, \
        Block VARCHAR, \
        Lot VARCHAR, \
        VolumeNumber VARCHAR, \
        UseCode VARCHAR, \
        UseDefinition VARCHAR, \
        PropertyClassCode VARCHAR, \
        PPropertyClassCodeDefinition VARCHAR, \
        YearPropertyBuilt INT(4), \
        NumberofBathrooms VARCHAR, \
        NumberofBedrooms VARCHAR, \
        NumberofRooms VARCHAR, \
        NumberofStories VARCHAR, \
        NumberofUnits VARCHAR, \
        ZoningCode VARCHAR, \
        ConstructionType VARCHAR, \
        LotDepth VARCHAR, \
        LotFrontage VARCHAR, \
        PropertyArea INT, \
        BasementArea INT, \
        LotArea INT, \
        LotCode VARCHAR, \
        TaxRateAreaCode VARCHAR, \
        PercentofOwnership VARCHAR, \
        ExemptionCode VARCHAR, \
        ExemptionCodeDefinition VARCHAR, \
        StatusCode VARCHAR, \
        MiscExemptionValue MONEY, \
        HomeownerExemptionValue MONEY, \
        CurrentSalesDate DATE, \
        AssessedFixturesValue MONEY, \
        AssessedImprovementValue MONEY, \
        AssessedLandValue MONEY, \
        AssessedPersonalPropertyValue MONEY, \
        AssessorNeighborhoodDistrict VARCHAR, \
        AssessorNeighborhoodCode VARCHAR, \
        AssessorNeighborhood VARCHAR, \
        SupervisorDistrict VARCHAR, \
        AnalysisNeighborhood VARCHAR, \
        RowID VARCHAR PRIMARY KEY \
)"

raw_csv_table_schema_sf = "CREATE UNLOGGED TABLE IF NOT EXISTS rawSFCountyTable ( \
        ClosedRollYear INT(4), \
        PropertyLocation VARCHAR, \
        ParcelNumber VARCHAR, \
        Block VARCHAR, \
        Lot VARCHAR, \
        VolumeNumber VARCHAR, \
        UseCode VARCHAR, \
        UseDefinition VARCHAR, \
        PropertyClassCode VARCHAR, \
        PPropertyClassCodeDefinition VARCHAR, \
        YearPropertyBuilt INT(4), \
        NumberofBathrooms VARCHAR, \
        NumberofBedrooms VARCHAR, \
        NumberofRooms VARCHAR, \
        NumberofStories VARCHAR, \
        NumberofUnits VARCHAR, \
        ZoningCode VARCHAR, \
        ConstructionType VARCHAR, \
        LotDepthVARCHAR, \
        LotFrontage VARCHAR, \
        PropertyArea INT, \
        BasementArea INT, \
        LotArea INT, \
        LotCode VARCHAR, \
        TaxRateAreaCode VARCHAR, \
        PercentofOwnership VARCHAR, \
        ExemptionCode VARCHAR, \
        ExemptionCode Definition VARCHAR, \
        StatusCode VARCHAR, \
        MiscExemptionValue MONEY, \
        HomeownerExemptionValue MONEY, \
        CurrentSalesDate DATE, \
        AssessedFixturesValue MONEY, \
        AssessedImprovementValue MONEY, \
        AssessedLandValue MONEY, \
        AssessedPersonalPropertyValue MONEY, \
        AssessorNeighborhoodDistrict VARCHAR, \
        AssessorNeighborhoodCode VARCHAR, \
        AssessorNeighborhood VARCHAR, \
        SupervisorDistrict VARCHAR, \
        AnalysisNeighborhood VARCHAR, \
        RowID VARCHAR PRIMARY KEY \
)"

# for API imports only
all_fields_socrata_sf = [
    'closed_roll_year',
    'property_location',
    'parcel_number',
    'block',
    'lot',
    'volume_number',
    'use_code',
    'use_definition',
    'property_class_code',
    'property_class_code_definition',
    'year_property_built',
    'number_of_bathrooms',
    'number_of_bedrooms',
    'number_of_rooms',
    'number_of_stories',
    'number_of_units',
    'zoning_code',
    'construction_type',
    'lot_depth',
    'lot_frontage',
    'property_area',
    'basement_area',
    'lot_area',
    'lot_code',
    'tax_rate_area_code',
    'percent_of_ownership',
    'exemption_code',
    'exemption_code_definition',
    'status_code',
    'misc_exemption_value',
    'homeowner_exemption_value',
    'current_sales_date',
    'assessed_fixtures_value',
    'assessed_improvement_value',
    'assessed_land_value',
    'assessed_personal_property_value',
    'assessor_neighborhood_district',
    'assessor_neighborhood_code',
    'assessor_neighborhood',
    'supervisor_district',
    'analysis_neighborhood',
    'row_id',
]

# for csv imports only
all_fields_csv_sf = [
        'Closed Roll Year',
        'Property Location',
        'Parcel Number',
        'Block',
        'Lot',
        'Volume Number',
        'Use Code',
        'Use Definition',
        'Property Class Code',
        'Property Class Code Definition',
        'Year Property Built',
        'Number of Bathrooms',
        'Number of Bedrooms',
        'Number of Room',
        'Number of Stories',
        'Number of Units',
        'Zoning Code',
        'Construction Type',
        'Lot Depth',
        'Lot Frontage',
        'Property Area',
        'Basement Area',
        'Lot Area',
        'Lot Code',
        'Tax Rate Area Code',
        'Percent of Ownership',
        'Exemption Code',
        'Exemption Code Definition',
        'Status Code',
        'Misc Exemption Value',
        'Homeowner Exemption Value',
        'Current Sales Date',
        'Assessed Fixtures Value',
        'Assessed Improvement Value',
        'Assessed Land Value',
        'Assessed Personal Property Value',
        'Assessor Neighborhood District',
        'Assessor Neighborhood Code',
        'Assessor Neighborhood',
        'Supervisor District',
        'Analysis Neighborhood',
        'Row ID',
]