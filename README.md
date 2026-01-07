

This program is designed to, given a series of user arguments, provide a list of US cities that would be viable for an MLB expansion team. This program provides a tool to broadly locate ideal expansion sites based on population, climate, and proximity to existing markets. This can help narrow down which cities may be viable for an MLB team.
This script is intended only to be viewed, not executed, and due to licensing issues does not include the data neccesary to run.

Arguments:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
To run this program, enter 5 user arguments in the following order:
1. The minimum distance the selected cities can be from an existing MLB stadium
2. The minimum population of the selected Combined Statistical Areas (CSA) NOTE: Once printed, the CSA names will be shortened to the major city within the CSA fo  ease of understanding
3. The highest the average maximum temperature can be during the MLB season in the selected city (in Fahrenheit)
4. The lowest the average minimum temperature can be during the MLB season in the selected city (in Fahrenheit)
5. The maximum monthly precipitation during the MLB season in the selected city (in inches)

The program will not run properly if these five arguments are not given in this order. If fewer than 5 arguments are provided, the script will prompt the user to input the required arguments in the console.
Example input: 90 2000000 90 45 6

Data:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
The purpose of this repository is to demonstrate my ability to write scripts with the ArcPy library, and it does not include a functional script. 

The data needed to run this script is not included due to licencing issues, however, the file names are included below. All files below are included in a folder titled "originalData".

tl_2023_us_csa.shp (and auxiliary files)

usa_csa_pop.csv

6 tif rasters beginning with tmax_

6 tif rasters beginning with tmin_

12 tif rasters beginning with pre_

Major_League_Baseball_Stadiums.shp (and auxiliary files)

Data Scources and Information:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. The CSA boundaries are from 2023 and come from the US Census Bureau
2. The CSA population table is from 2024 and comes from the US Census Bureau
3. The maximum temperature, minimum temperature, and precipitation rasters all come from WorldClim.

(There are six average maximum temperature rasters for the months June, July, and August of 2020 and 2021. These represent the hottest months of two recent MLB seasons
The raster data is in Celsius, but user inputs and the displayed information are converted to Fahrenheit)

(There are six average minimum temperature rasters for the months April, May, and September of 2020 and 2021. These represent the coldest months of two recent MLB seasons
The raster data is in Celsius, but user inputs and the displayed information are converted to Fahrenheit)

(There are 12 average monthly precipitation rasters for the months April through September of 2020 and 2021.
The raster data is in millimeters, but user inputs and the displayed information are converted to inches)

4. The MLB Stadiums Shapefile is from ESRI ArcGIS Hub and is accurate as of the 2025 MLB season
