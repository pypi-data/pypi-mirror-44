class PlantPredictEnum(dict):
    pass


# Air Mass Model
air_mass_model_type_enum = PlantPredictEnum()
air_mass_model_type_enum.BIRD_HULSTROM = 0
air_mass_model_type_enum.KASTEN_SANDIA = 1

# Backtracking Type
backtracking_type_enum = PlantPredictEnum()
backtracking_type_enum.TRUE_TRACKING = 0   # no backtracking
backtracking_type_enum.BACKTRACKING = 1    # shade avoidance

# Cell Technology
cell_technology_type_enum = PlantPredictEnum()
cell_technology_type_enum.NTYPE_MONO_CSI = 1
cell_technology_type_enum.PTYPE_MONO_CSI_PERC = 2
cell_technology_type_enum.PTYPE_MONO_CSI_BSF = 3
cell_technology_type_enum.POLY_CSI_PERC = 4
cell_technology_type_enum.POLY_CSI_BSF = 5
cell_technology_type_enum.CDTE = 6
cell_technology_type_enum.CIGS = 7

# Cleaning Frequency
cleaning_frequency_enum = PlantPredictEnum()
cleaning_frequency_enum.NONE = 0
cleaning_frequency_enum.DAILY = 1
cleaning_frequency_enum.MONTHLY = 2
cleaning_frequency_enum.QUARTERLY = 3
cleaning_frequency_enum.YEARLY = 4

# Construction Type
construction_type_enum = PlantPredictEnum()
construction_type_enum.GLASS_GLASS = 1
construction_type_enum.GLASS_BACKSHEET = 2

# Data Source
data_source_enum = PlantPredictEnum()
data_source_enum.MANUFACTURER = 1
data_source_enum.PVSYST = 2
data_source_enum.UNIVERSITY_OF_GENEVA = 3
data_source_enum.PHOTON = 4
data_source_enum.SANDIA_DATABASE = 5
data_source_enum.CUSTOM = 6

# Degradation Model
degradation_model_enum = PlantPredictEnum()
degradation_model_enum.NONE = 0
degradation_model_enum.STEPPED_AC = 1
degradation_model_enum.LINEAR_AC = 2
degradation_model_enum.LINEAR_DC = 3
degradation_model_enum.NON_LINEAR_DC = 4

# Diffuse Direct Decomposition Model
diffuse_direct_decomposition_model_enum = PlantPredictEnum()
diffuse_direct_decomposition_model_enum.ERBS = 0
diffuse_direct_decomposition_model_enum.REINDL = 1
diffuse_direct_decomposition_model_enum.DIRINT = 2
diffuse_direct_decomposition_model_enum.NONE = 3

# Diffuse Shading Model
diffuse_shading_model_enum = PlantPredictEnum()
diffuse_shading_model_enum.NONE = 0
diffuse_shading_model_enum.SCHAAR_PANCHULA = 1

# Direct Beam Shading Model
direct_beam_shading_model_enum = PlantPredictEnum()
direct_beam_shading_model_enum.LINEAR = 0
direct_beam_shading_model_enum.NONE = 1
direct_beam_shading_model_enum.TWO_DIMENSION = 2   # Retired
direct_beam_shading_model_enum.FRACTIONAL_EFFECT = 3   # Fractional Electric Shading
direct_beam_shading_model_enum.CSI_3_DIODE = 4
direct_beam_shading_model_enum.MODULE_FILE_DEFINED = 5

# Entity Type
entity_type_enum = PlantPredictEnum()
entity_type_enum.PROJECT = 1
entity_type_enum.MODULE = 2
entity_type_enum.INVERTER = 3
entity_type_enum.WEATHER = 4
entity_type_enum.PREDICTION = 5

# Energy Storage System (ESS) Charge Algorithm
ess_charge_algorithm_enum = PlantPredictEnum()
ess_charge_algorithm_enum.LGIA_EXCESS = 0
ess_charge_algorithm_enum.ENERGY_AVAILABLE = 1
ess_charge_algorithm_enum.CUSTOM = 2

# Energy Storage System (ESS) Dispatch Custom Command
ess_dispatch_custom_command_enum = PlantPredictEnum()
ess_dispatch_custom_command_enum.NONE = 0
ess_dispatch_custom_command_enum.DISCHARGE = 1
ess_dispatch_custom_command_enum.CHARGE = 2

# Faciality
faciality_enum = PlantPredictEnum()
faciality_enum.MONOFACIAL = 0
faciality_enum.BIFACIAL = 1

# Incidence Angle Model Type
incidence_angle_model_type_enum = PlantPredictEnum()
incidence_angle_model_type_enum.SANDIA = 2
incidence_angle_model_type_enum.ASHRAE = 3
incidence_angle_model_type_enum.NONE = 4
incidence_angle_model_type_enum.TABULAR_IAM = 5

# Library Status
library_status_enum = PlantPredictEnum()
library_status_enum.UNKNOWN = 0
library_status_enum.DRAFT_PRIVATE = 1
library_status_enum.DRAFT_SHARED = 2
library_status_enum.ACTIVE = 3
library_status_enum.RETIRED = 4
library_status_enum.GLOBAL = 5
library_status_enum.GLOBAL_RETIRED = 6

# Module Degradation Model
module_degradation_model_enum = PlantPredictEnum()
module_degradation_model_enum.UNSPECIFIED = 0
module_degradation_model_enum.LINEAR = 1
module_degradation_model_enum.NONLINEAR = 2

# Module Orientation
module_orientation_enum = PlantPredictEnum()
module_orientation_enum.LANDSCAPE = 0
module_orientation_enum.PORTRAIT = 1

# Module Shading Response
module_shading_response_enum = PlantPredictEnum()
module_shading_response_enum.NONE = 0
module_shading_response_enum.LINEAR = 1
module_shading_response_enum.FRACTIONAL_EFFECT = 2   # Fractional Electrical Shading
module_shading_response_enum.CSI_3_DIODE = 3
module_shading_response_enum.CUSTOM = 4

# Module Temperature Model
module_temperature_model_enum = PlantPredictEnum()
module_temperature_model_enum.HEAT_BALANCE = 0
module_temperature_model_enum.SANDIA = 1

# Module Type
module_type_enum = PlantPredictEnum()
module_type_enum.SINGLE_DIODE = 0
module_type_enum.ADVANCED_DIODE = 1

# Prediction Status
prediction_status_enum = PlantPredictEnum()
prediction_status_enum.DRAFT_PRIVATE = 1
prediction_status_enum.DRAFT_SHARED = 2
prediction_status_enum.ANALYSIS = 3
prediction_status_enum.BID = 4
prediction_status_enum.CONTRACT = 5
prediction_status_enum.DEVELOPMENT = 6
prediction_status_enum.AS_BUILT = 7
prediction_status_enum.WARRANTY = 8
prediction_status_enum.ARCHIVED = 9

# Prediction Version
prediction_version_enum = PlantPredictEnum()
prediction_version_enum.VERSION_3 = 3
prediction_version_enum.VERSION_4 = 4
prediction_version_enum.VERSION_5 = 5
prediction_version_enum.VERSION_6 = 6
prediction_version_enum.VERSION_7 = 7

# Processing Status
processing_status_enum = PlantPredictEnum()
processing_status_enum.NONE = 0
processing_status_enum.QUEUED = 1
processing_status_enum.RUNNING = 2
processing_status_enum.SUCCESS = 3
processing_status_enum.ERROR = 4

# Project Status
project_status_enum = PlantPredictEnum()
project_status_enum.ACTIVE = 0
project_status_enum.ARCHIVED = 1

# PV Model
pv_model_type_enum = PlantPredictEnum()
pv_model_type_enum.ONE_DIODE_RECOMBINATION = 0
pv_model_type_enum.ONE_DIODE = 1
pv_model_type_enum.ONE_DIODE_RECOMBINATION_NONLINEAR = 3

# Soiling Model
soiling_model_type_enum = PlantPredictEnum()
soiling_model_type_enum.CONSTANT_MONTHLY = 0
soiling_model_type_enum.WEATHER_FILE = 1
soiling_model_type_enum.NONE = 2

# Spectral Shift Model
spectral_shift_model_enum = PlantPredictEnum()
spectral_shift_model_enum.NO_SPECTRAL_SHIFT = 0
spectral_shift_model_enum.ONE_PARAM_PWAT_OR_SANDIA = 1
spectral_shift_model_enum.TWO_PARAM_PWAT_AND_AM = 2
spectral_shift_model_enum.MONTHLY_OVERRIDE = 3

# Spectral Weather Type
spectral_weather_type_enum = PlantPredictEnum()
spectral_weather_type_enum.NONE = 0
spectral_weather_type_enum.NGAN_PWAT = 1
spectral_weather_type_enum.NGAN_RH = 2
spectral_weather_type_enum.NGAN_DEWPOINT = 3

# Tracking Type
tracking_type_enum = PlantPredictEnum()
tracking_type_enum.FIXED_TILT = 0
tracking_type_enum.HORIZONTAL_TRACKER = 1
tracking_type_enum.SEASONAL_TILT = 2

# Transposition Model
transposition_model_enum = PlantPredictEnum()
transposition_model_enum.HAY = 0
transposition_model_enum.PEREZ = 1

# Weather Data Provider
weather_data_provider_enum = PlantPredictEnum()
weather_data_provider_enum.NREL = 1
weather_data_provider_enum.AWS = 2
weather_data_provider_enum.WIND_LOGICS = 3
weather_data_provider_enum.METEONORM = 4
weather_data_provider_enum.THREE_TIER = 5
weather_data_provider_enum.CLEAN_POWER_RESEARCH = 6
weather_data_provider_enum.GEO_MODEL_SOLAR = 7
weather_data_provider_enum.GEO_SUN_AFRICA = 8
weather_data_provider_enum.SODA = 9
weather_data_provider_enum.HELIO_CLIM = 10
weather_data_provider_enum.SOLAR_RESOURCE_ASSESSMENT = 11
weather_data_provider_enum.ENERGY_PLUS = 12
weather_data_provider_enum.OTHER = 13
weather_data_provider_enum.CUSTOMER = 14
weather_data_provider_enum.SOLAR_PROSPECTOR = 15
weather_data_provider_enum.GLOBAL_FED = 16
weather_data_provider_enum.NSRDB = 17
weather_data_provider_enum.WHITE_BOX_TECHNOLOGIES = 18
weather_data_provider_enum.SOLARGIS = 19
weather_data_provider_enum.NASA = 20

# Weather Data Type
weather_data_type_enum = PlantPredictEnum()
weather_data_type_enum.SYNTHETIC_MONTHLY = 0
weather_data_type_enum.SATELLITE = 1
weather_data_type_enum.GROUND_CORRECTED = 2
weather_data_type_enum.MEASURED = 3
weather_data_type_enum.MY3 = 4
weather_data_type_enum.TGY = 5
weather_data_type_enum.TMY = 6
weather_data_type_enum.PSM = 7
weather_data_type_enum.SUNY = 8
weather_data_type_enum.MTS2 = 9
weather_data_type_enum.CZ2010 = 10

# Weather File Column Type
weather_file_column_type = PlantPredictEnum()
weather_file_column_type.GHI = 1
weather_file_column_type.DNI = 2
weather_file_column_type.DHI = 3
weather_file_column_type.TEMP = 4
weather_file_column_type.WINDSPEED = 5
weather_file_column_type.RELATIVE_HUMIDITY = 6
weather_file_column_type.PWAT = 7
weather_file_column_type.RAIN = 8
weather_file_column_type.PRESSURE = 9
weather_file_column_type.DEWPOINT_TEMP = 10
weather_file_column_type.WIND_DIRECTION = 11
weather_file_column_type.SOILING_LOSS = 12
weather_file_column_type.POAI = 13

# Weather P-Level
weather_plevel_enum = PlantPredictEnum()
weather_plevel_enum.P50 = 0
weather_plevel_enum.P90 = 1
weather_plevel_enum.P95 = 3
weather_plevel_enum.P99 = 4
weather_plevel_enum.NA = 2      # N/A
weather_plevel_enum.P75 = 5

# Weather Time Resolution
weather_time_resolution_enum = PlantPredictEnum()
weather_time_resolution_enum.UNKNOWN = 0
weather_time_resolution_enum.HALF_HOUR = 1
weather_time_resolution_enum.HOUR = 2
weather_time_resolution_enum.MINUTE = 3
