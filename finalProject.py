# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# finalProject.py
# Created on: 2016-04-24 17:27:32.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# Clip bear nuisances to area,  find the mean circle
# ---------------------------------------------------------------------------

# import system module
import sys
# Import arcpy module
import arcpy

# import BearNuisance functions
import BearNuisance

# Set Geoprocessing environments
#arcpy.env.workspace = "C:\\Users\\mdeeds\\Documents\\Mayer\\FRCC\\GIS210_Intermediate\\FinalProject\\BearNuisance.gdb"
arcpy.env.workspace = "C:\\Users\\mdeeds\\Documents\\Mayer\\FRCC\\GIS210_Intermediate\\FinalProject\\BearNuisanceRun.gdb"

print "Workspace is : {0}".format(arcpy.env.workspace)

# enable overwriting
arcpy.env.overwriteOutput = True

#----------------------------------------------------------
# Variables for selecting housing parcels and make a layer
#----------------------------------------------------------
# The merged 5 county parcel data
countyParcelsMerge = "countyParcelsMerge"

# Merged parcel data with Single Family Houses selected
countyParcelsMerge_Houses = "countyParcelsMerge_Select"

# Housing Parcel Layer
countyParcelsMerge_Houses_Layer = "countyParcelsMerge_Houses_Layer"

#-------------------------------------------
# Variables for making bear nuisance tiers
#-------------------------------------------
# Black bear area of interest
Bear_AOI = "Bear_AOI"
#Bear_AOI = "Bear_AOIxxxxxxxxxxx"  # to check for missing data

# Black bear nuisance reports points
Black_Bear_Nuisance_Reports = "Black_Bear_Nuisance_Reports"

#----------------------------------------------------------
# for intersecting bear density tiers with housing parcels
#----------------------------------------------------------
housesFC = "countyParcelsMerge_Select"

bearFC =  "BearNuisKD_reclass_poly"

# check the 3 input files :
if not (arcpy.Exists(Bear_AOI) and arcpy.Exists(Black_Bear_Nuisance_Reports) and arcpy.Exists(countyParcelsMerge)) :
    print "There is missing data!! Exiting"
    sys.exit(1)


# try to selected houses from merged county layer and then making a layer from the selection
try :

    # Don't select houses if the data already exists (this select is slow)
    if (not (arcpy.Exists(countyParcelsMerge_Houses)) ) :
        # Select Single House parcels from County Merge data
        # Process: Select
        print "Selecting housing parcels from " + countyParcelsMerge + " and saving to " + countyParcelsMerge_Houses
        arcpy.Select_analysis(countyParcelsMerge, countyParcelsMerge_Houses, "DESCRIPT = 'SINGLE FAMILY'")

    # Make a feature layer from Housing Parcels
    ## Process: Make Feature Layer
    print "Making feature layer from " + countyParcelsMerge_Houses + " as layer : " + countyParcelsMerge_Houses_Layer
    # MakeFeatureLayer_management (in_features, out_layer, {where_clause}, {workspace}, {field_info})
    arcpy.MakeFeatureLayer_management(countyParcelsMerge_Houses, countyParcelsMerge_Houses_Layer)

except arcpy.ExecuteError :
    print arcpy.GetMessages(2)
    sys.exit(1)

except Exception, err:
    sys.stderr.write('ERROR: %s' % str(err))
    sys.exit(1)

# Make Bear Nuisance Density : 4 tiers
BearNuisance.MakeDensityTiers(Bear_AOI, Black_Bear_Nuisance_Reports)

# Find parcels that intersect each tier
BearNuisance.IntersectTierParcels(housesFC, bearFC)
