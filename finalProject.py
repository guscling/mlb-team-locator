####View README.md for an in-depth explanation of the script and it's data

import os, sys
try:
    import arcpy

except ImportError:
    raise ImportError(
        "ArcPy is required to run this script. "
        "An ArcGIS Pro licensed environment is required."
    )

#Set up relative paths/directory
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "originalData")
created_data_dir = os.path.join(script_dir,"createdData")

required_paths = [
    data_dir,
    os.path.join(data_dir, "tl_2023_us_csa.shp"),
    os.path.join(data_dir, "usa_csa_pop.csv"),
    os.path.join(data_dir, "Major_League_Baseball_Stadiums.shp")
]

for path in required_paths:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Required data not found: {path}\n"
            "See README.md for required data structure."
        )
    

# If run without command-line arguments, prompt user for input instead
if len(sys.argv) != 6:
    print("Too few system arguments detected. Please enter the required parameters.\n")

    try:
        dist = input("1. The minimum distance allowed from an existing MLB stadium (mi): ")
        pop = input("2. The minimum population of the CSA: ")
        max_temp = input("3. The maximum allowed average high temperature (°F): ")
        min_temp = input("4. The minimum allowed average low temperature (°F): ")
        precip = input("5. The maximum monthly precipitation (inches): ")

        # Replace sys.argv with the values the user entered
        sys.argv = [
            sys.argv[0],  # script name placeholder
            dist,
            pop,
            max_temp,
            min_temp,
            precip
        ]

    except Exception as e:
        print("Invalid input. Using default parameters instead.")
        sys.argv = [sys.argv[0], "90", "2000000", "90", "45", "6"]

#Replaces all existing files when the script is rerun
arcpy.env.overwriteOutput = True

#Create a directory for the created data if one does not exist
if not os.path.exists(created_data_dir):
    os.mkdir(created_data_dir)

arcpy.env.workspace = created_data_dir

csa_boundaries_path = os.path.join(data_dir,"tl_2023_us_csa.shp")
csa_population_table= os.path.join(data_dir,"usa_csa_pop.csv")

#Save the CSA boundaries as a new feature layer
arcpy.management.MakeFeatureLayer(csa_boundaries_path, "csa_poly_layer")

#Join the CSA population to the CSA boundaries
arcpy.management.AddJoin("csa_poly_layer","NAME",csa_population_table,"CMA_Name")

#Convert the CSA boundaries to point features and save as a new layer
arcpy.management.FeatureToPoint("csa_poly_layer","csa_points")
arcpy.management.MakeFeatureLayer("csa_points", "csa_points_layer")

#Remove the previous join to prevent issues with field names
arcpy.management.RemoveJoin("csa_poly_layer")

#Allows you to use the spatial analyst tools in ArcGIS Pro
arcpy.CheckOutExtension("Spatial")

#Set the working directory to the original data folder
arcpy.env.workspace = data_dir

#average and save max temp rasters
max_rasters = arcpy.ListRasters("tmax_*","TIF")

sum_max_rasters = None
max_count = 0
#Add the rasters to each other and divides by the number of rasters. In this case, the rasters used will always be the same
for raster in max_rasters:
    if sum_max_rasters is None:
        sum_max_rasters = arcpy.Raster(raster)
    else:
        sum_max_rasters = sum_max_rasters + arcpy.Raster(raster)
    max_count += 1

max_mean_raster = sum_max_rasters / max_count
#Saves the raster as a tif files in the created data folder
max_raster_path = os.path.join(created_data_dir,"max_mean_raster.tif")
max_mean_raster.save(max_raster_path)

#average and save min temp rasters
min_rasters = arcpy.ListRasters("tmin_*","TIF")

sum_min_rasters = None
min_count = 0

for raster in min_rasters:
    if sum_min_rasters is None:
        sum_min_rasters = arcpy.Raster(raster)
    else:
        sum_min_rasters = sum_min_rasters + arcpy.Raster(raster)
    min_count += 1

min_mean_raster = sum_min_rasters / min_count
min_raster_path = os.path.join(created_data_dir,"min_mean_raster.tif")
min_mean_raster.save(min_raster_path)

#average and save precipitation rasters
precip_rasters = arcpy.ListRasters("pre_*","TIF")

sum_precip_rasters = None
precip_count = 0

for raster in precip_rasters:
    if sum_precip_rasters is None:
        sum_precip_rasters = arcpy.Raster(raster)
    else:
        sum_precip_rasters = sum_precip_rasters + arcpy.Raster(raster)
    precip_count += 1

precip_mean_raster = sum_precip_rasters / precip_count
precip_raster_path = os.path.join(created_data_dir,"precip_mean_raster.tif")
precip_mean_raster.save(precip_raster_path)

#Set the working directory back to the created data folder. Extract the raster values to the CSA points and save it as a layer
arcpy.env.workspace = created_data_dir
arcpy.sa.ExtractMultiValuesToPoints("csa_points", [[max_raster_path, "max_mean_raster"],[min_raster_path,"min_mean_raster"],[precip_raster_path, "precip_mean_raster"]])
arcpy.MakeFeatureLayer_management("csa_points", "csa_points_layer")

#Buffer the MLB Stadium shapefile based on the user argument
mlb_stadiums = os.path.join(data_dir,"Major_League_Baseball_Stadiums.shp")
arcpy.analysis.Buffer(mlb_stadiums, "mlb_buffer",f"{sys.argv[1]} Miles")

#Select all features in CSA points that are not within the buffer around the MLB stadiums
arcpy.management.SelectLayerByLocation("csa_points_layer","INTERSECT", "mlb_buffer", invert_spatial_relationship="INVERT")

#Adding to the existing selection, select only features that meet the criteria laid out in the user arguments
#The user arguments are converted from Fahrenheit and inches to Celsius and millimeters, which the data is in
user_arguments = [float(sys.argv[2]),(float(sys.argv[3]) - 32) * (5/9),(float(sys.argv[4]) - 32) * (5/9),float(sys.argv[5])*25.4]
field_names = ["usa_csa__1","max_mean_r","min_mean_r","precip_mea"]
boolean_operators = [">=","<=",">=","<="]

for field,operator,argument in zip(field_names,boolean_operators,user_arguments):
    delimited = arcpy.AddFieldDelimiters("csa_points_layer",field)
    arcpy.management.SelectLayerByAttribute("csa_points_layer","SUBSET_SELECTION",f"{delimited} {operator} {argument}")

#Save the selected cities as a new layer in the created data folder
selected_cities = os.path.join(created_data_dir,"selected_cities.shp")
arcpy.management.CopyFeatures("csa_points_layer", selected_cities)

#Iterate through the selected layers and print the names of and information about the cities that meet the given criteria
cursor_fields = ["usa_csa_po","usa_csa__1","max_mean_r","min_mean_r","precip_mea"] #filed names are capped at 10 characters
with arcpy.da.SearchCursor(selected_cities, cursor_fields) as cursor:
    for row in cursor:
        #Takes the name of only the most populous city in the CSA
        if row[0].split(',')[1].count('-') > 0:
            print(f"{row[0].split(',')[0].split('-')[0]},{row[0].split(',')[1].split('-')[0]}")
        else:
            print(f"{row[0].split(',')[0].split('-')[0]},{row[0].split(',')[1]}")
        print(
            f"Population: {row[1]:,}\n"
            #Converts the displayed data to Fahrenheit and inches
            f"Average Maximum Temperature During Season: {(float(row[2]) * 9 / 5) + 32:.2f} °F\n"
            f"Average Minimum Temperature During Season: {(float(row[3]) * 9 / 5) + 32:.2f} °F\n"
            f"Average Precipitation During Season: {float(row[4]) / 25.4:.2f} inches\n\n\n"
        )
