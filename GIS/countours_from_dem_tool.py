"""
This script creates countours from a DEM raster dataset in ArcGIS Pro
"""

import arcpy

#Set input raster
input_dem = "set input dem raster path here"

#Set output
output_contours = "set countour feature class path here"

#Set contour interval here in meters
contour_interval = 25

#Set base contour level
base_contour = 0

#Check out spatial analyst extension
arcpy.CheckOutExtension("Spatial")

try:
    # Run contour tool
    arcpy.sa.Contour(input_dem, output_contours, contour_interval, base_contour)

    #If successful, print statement
    print("Contour lines created!")

except arcpy.ExecuteError:
    #If unsuccessful, print error messages
    print(arcpy.GetMessages(2))

finally:
    #Check in spatial analyst extension
    arcpy.CheckInExtension("Spatial")