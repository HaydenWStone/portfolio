"""
This script reads GPS lap track points from a CSV and creates a polyline feature class for individual laps
"""

import arcpy
import csv
import os

#Set input CSV location
csv_location = "set here"

#Set output location
out_path = "set here"

#Open CSV
with open(csv_location, "r") as file:

    #Create CSV reader object
    reader = csv.DictReader(file, delimiter=",")

    #Create dictionary to store points for each lap
    lap_dicts = {}

    #Read CSV
    for row in reader:

        # Skip lap time and end session lines
        if row["Time"].startswith("#"):
            if row["Time"].startswith("#'):
                continue
            print(row["Time"])
            continue

        #Add each point to lap list
        lap_num = int(row["Lap"])
        lap_dict = lap_dicts.setdefault(lap_num, [])
        lap_dict.append((float(row["Latitude"]), float(row["Longitude"])))

    #Delete data for first and last lap
    del lap_dicts[0]
    del lap_dicts[len(lap_dicts)]

#Create new polyline feature class with WGS84
spatial_reference = arcpy.SpatialReference(4326)
arcpy.management.CreateFeatureclass(os.path.dirname(out_path), os.path.basename(out_path), "POLYLINE", spatial_reference=spatial_reference)

#Add LapNumber field to feature class
arcpy.management.AddField(out_path, "LapNumber", "SHORT")

# Create polylines from laps in dictionary
with arcpy.da.InsertCursor(out_path, ["SHAPE@", "LapNumber"]) as cursor:
    for lap_num, lap_points in lap_dicts.items():
        polyline_array = arcpy.Array([arcpy.Point(point[1], point[0]) for point in lap_points])
        polyline = arcpy.Polyline(polyline_array, spatial_reference)
        cursor.insertRow([polyline, lap_num])
