# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:49:08 2020

@author: Rafael G. de Menezes
Oceanographer, Msc. Marine Biotechnology

Clube do Cientista
Biosustente Estudos Ambientais ltda.

README:
    Python function to transform google earth .kml files list into a pandas DataFrame 
    Necessary function for the 'Mapping_kml' code (https://github.com/rafaelgmenezes/Mapping_kml)
    
    .kml files location:
        folder in current working directory
        or files directly in current working directory
    
    dataFrame ouput content: 
        Filename -> the .kml filename 
        Lon      -> meridians coordinate
        Lat      -> parallels coordinate
    output options: 
        fmt = 'df'   -> a DataFrame object  (default)
        fmt = 'csv'  -> save DataFrame in a .csv file
        fmt = 'both' -> both outputs options above
"""

def kml_to_df (fmt = 'df'):    # fmt = output format 
   fmt_options = ['df', 'csv', 'both']
   if fmt not in fmt_options:
       print ("'fmt' options:")
       [print (f) for f in fmt_options]
       print ("default = 'df'")
       raise NameError("fmt argument is not set properly")           
    
   import os
   from glob import glob
   path = os.getcwd()
   if len (glob('*.kml')) == 0:
       try:
           os.chdir('kmlfiles')   
       except:
           try:
               os.chdir('kmlbase')
           except FileNotFoundError:
                raise FileNotFoundError ('kml files were not found')

   from bs4 import BeautifulSoup
   import pandas as pd
   
   kml_list = glob('*.kml')
   df = pd.DataFrame(columns = ['Filename', 'Lon', 'Lat'])
   remove_chars = ['[',']','<','>','\n','\t','coordinates', '/']

   for file in kml_list:
       with open(file, 'r') as f:
          soup = BeautifulSoup(f, features = "html.parser")
          node = soup.select('coordinates')
          coords = str(node)
          for char in remove_chars:
              coords = coords.replace(char,'')

          dfi = {'Lon': [], 'Lat': []}
          for j in list(coords[:-1].split(' ')):
              c = j.split(',')
              dfi['Lon'].append(float(c[0]))
              dfi['Lat'].append(float(c[1]))
       f.close()
       
       dfi = pd.DataFrame(dfi)
       dfi['Filename'] = file.split('.')[0]
       df = pd.concat([df,dfi], axis = 0, sort = False)
   df = df.reset_index(drop = True)
   
   print('\nkml files located at :\n', os.getcwd(), '\n were properly converted')
   os.chdir(path)
   if fmt == 'csv':
       df.to_csv('kml_to_df_output.csv')
   elif fmt == 'df':
       return df
   if fmt == 'both':
       df.to_csv('kml_to_df_output.csv')
       return df
