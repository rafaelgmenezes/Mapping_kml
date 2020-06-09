# Mapping_kml
Functions to make maps from .kml files using matplotlib and kml_to_df

README:
    Making maps with .KML files (from Google Earth) using Matplotlib. 
    Reccomended for LOCAL SCALE, for larger scales, basemap resolution looks fine.
    INTERACTIVE script to select .kml files folder to plot.
    
    kml_to_df.py file is required to transform .kml files to a pandas DataFrame.
    kml_to_df readme -> https://github.com/rafaelgmenezes/kml_to_df
    
    CURRENT WORKING DIRECTORY is expected to be the same as the location of this file (Mapping_kml.py)
    .KML FILES FOLDER (kmlbase) is expected to be at the same as the location of this file (Mapping_kml.py)
    
    EXAMPLES:
        Arraial do Cabo, RJ, southeast Brazil
        Fernando de Noronha, PE, northeast Brazil
       
    To plot other kml files, just create a new folder and chose it during interaction.
         
    DEFAULTS:
    FIGURE SIZE -> default to best fit into a 15.6" notebook screen 
    AUTOSCALE   -> in kilometers (km) and designed to fit axis sizes. 
                   location and number of kilometers can be set at line 206
    SAVE FIGURE -> figure will be saved at the current working directory
                   default -> .png and 200 dpi
