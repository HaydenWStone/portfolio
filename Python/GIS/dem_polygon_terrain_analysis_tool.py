"""
This script tool accepts an input DEM and polygon shapefile, clips the DEM to each polygon, then generates a hillshade raster,
a slope raster, and 10m contours for each polygon. The script then produces a PDF book of each hillshade image with
a title and text showing the area of the polygon in square kilometers. The script was developed to analyze Federal wilderness areas but could
be used for any polygon feature class and accompanying DEM.

The script is designed to be used a tool in ArcGIS Pro
"""

#Import packages
import arcpy
from arcpy.sa import *
from PIL import Image, ImageOps, ImageDraw, ImageFont
import os
import urllib.request

#Define input parameters
input_fc = arcpy.GetParameterAsText(0)
input_dem = arcpy.GetParameterAsText(1)
output_folder = arcpy.GetParameterAsText(2)

#Download font for image text for book
url = "http://themes.googleusercontent.com/static/fonts/abel/v3/N59kklKPso9WzbZH9jwJSg.ttf"
font_path = "temp_font.ttf"
urllib.request.urlretrieve(url, font_path)
area_text = ""
images = []

#Check out Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

#Set workspace
arcpy.env.workspace = output_folder

#Path name cleaner function
def sanitize_name(name):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    return "".join(c for c in name if c in valid_chars)

#Loop through each polygon in the input feature class
with arcpy.da.SearchCursor(input_fc, ["SHAPE@", "Name"]) as cursor:
    for row in cursor:
        proper_name = row[1]
        poly_name = sanitize_name(row[1])
        print(f"Processing polygon {proper_name}")
        arcpy.AddMessage(f"Processing polygon {proper_name}")

        #Clip the DEM to the polygon
        print("Clipping DEM")
        arcpy.AddMessage("Clipping DEM")
        clip_dem = arcpy.Clip_management(
            in_raster=input_dem,
            rectangle="#",
            out_raster=f"{output_folder}\\{poly_name}_clipped_dem.tif",
            in_template_dataset=row[0],
            nodata_value="0",
            clipping_geometry="ClippingGeometry",
            maintain_clipping_extent="NO_MAINTAIN_EXTENT"
        )

        try:
            #Create hillshade for the clipped DEM
            print("Creating hillshade raster")
            arcpy.AddMessage("Creating hillshade raster")
            hillshade_raster = Hillshade(clip_dem)
            hillshade_raster.save(f"{output_folder}\\{poly_name}_hillshade.tif")
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            #Create slope for the clipped DEM
            print("Creating slope raster")
            arcpy.AddMessage("Creating slope raster")
            slope_raster = Slope(clip_dem)
            slope_raster.save(f"{output_folder}\\{poly_name}_slope.tif")
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            #Create 10m contours for the clipped DEM
            print("Generating contours")
            arcpy.AddMessage("Generating contours")
            contours_output = f"{output_folder}\\{poly_name}_contours.shp"
            arcpy.Contour_3d(clip_dem, contours_output, 10)
        except Exception as e:
            print(f"An error occurred: {e}")

            #Calculate polygon area
        try:
            poly_geom = row[0]
            poly_area = round((poly_geom.area) / 1000000, 2)
            area_text = (f"{poly_area} square km")
            print(area_text)
            arcpy.AddMessage(area_text)
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            #Create PNG from hillshade TIF
            with Image.open(f"{output_folder}\\{poly_name}_hillshade.tif") as img:
                Image.MAX_IMAGE_PIXELS = None
                img_l = ImageOps.autocontrast(img)
                img_l.save(f"{output_folder}\\{poly_name}_hillshade.png", 'PNG')
                print("Hillshade PNG created")
                arcpy.AddMessage("Hillshade PNG created")

                #Resize PNG
                image = Image.open(f"{output_folder}\\{poly_name}_hillshade.png")
                max_width = 10000  # Set the max width you want for the images
                max_height = 10000  # Set the max height you want for the images
                img_width, img_height = image.size
                aspect_ratio = float(img_width) / float(img_height)
                new_width = min(max_width, img_width)
                new_height = int(new_width / aspect_ratio)
                if new_height > max_height:
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)
                resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
                resized_image.save(f"{output_folder}\\{poly_name}_hillshade_resized.png")
                image.close()
                resized_image.close()
                os.remove(f"{output_folder}\\{poly_name}_hillshade.png")
                print("Image resized")
                arcpy.AddMessage("Image resized")

                #Write title and area on PNG
                image = Image.open(f"{output_folder}\\{poly_name}_hillshade_resized.png")
                width, height = image.size
                draw = ImageDraw.Draw(image)
                font_size = 150
                font = ImageFont.truetype(font_path, font_size)
                color = 0
                draw.text((150, 200), proper_name, font=font, fill=color)
                draw.text((150, 400), area_text, font=font, fill=color)
                image.save(f"{output_folder}\\{poly_name}_hillshade.png")
                image.close()
                os.remove(f"{output_folder}\\{poly_name}_hillshade_resized.png")
                print("Title added")
                arcpy.AddMessage("Title added")

        except Exception as e:
            print(f"An error occurred: {e}")

#Create PDF book
try:
    #Get a list of all the hillshade PNGs
    png_files = [f for f in os.listdir(output_folder) if f.endswith('.png')]
    png_files.sort()
    images = []
    #Loop through PNGS and append to list
    for png_file in png_files:
        images.append(Image.open(os.path.join(output_folder, png_file)))
    #Create PDF map book
    print("Creating PDF")
    arcpy.AddMessage("Creating PDF")
    pdf_file = fr"{output_folder}\hillshade_map_book.pdf"
    images[0].save(pdf_file, save_all=True, append_images=images[1:])
    print(f"PDF created at {pdf_file}")
    arcpy.AddMessage(f"PDF created at {pdf_file}")

except Exception as e:
    print(f"An error occurred: {e}")

#Check in the Spatial Analyst extension license
arcpy.CheckInExtension("Spatial")


