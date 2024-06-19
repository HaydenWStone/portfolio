
"""
This script preforms batch reprojections for feature classes in a folder to match the projection of a target feature class
"""

import arcpy

#Set initial conditions
arcpy.env.overwriteOutput = True
target_folder = arcpy.GetParameterAsText(0)
target_dataset = arcpy.GetParameterAsText(1)
files_str = ""

# Get the target dataset's projection
target_reference = arcpy.Describe(target_dataset).spatialReference
target_reference_name = arcpy.Describe(target_dataset).spatialReference.name

#Define workspace
arcpy.env.workspace = target_folder

#Get list of feature classes
files = arcpy.ListFeatureClasses()

#Main loop
for file in files:

    try:
        #Create file path string for input file
        path = target_folder + "/" + file

        # Get the input dataset's projection
        input_reference_name = arcpy.Describe(path).spatialReference.name

        #If input dataset's projection does not match the target projection
        if input_reference_name != target_reference_name:
            #Create new file path
            new_path = path.rsplit(".", 1)[0] + "_projected." + path.rsplit(".", 1)[1]

            #Preform the reprojection
            arcpy.management.Project(path,new_path,target_reference)

            #Add file name to list
            files_str += (file + ", ")

    except:
        # If unsuccessful, print error messages
        print(arcpy.GetMessages(2))

#Strip trailing comma and space from the list of files
files_str = files_str[:-2]

#Report which files were projected
arcpy.AddMessage(f"Reprojected {files_str} to {target_reference_name}")
print(f"Reprojected {files_str} to {target_reference_name}")
