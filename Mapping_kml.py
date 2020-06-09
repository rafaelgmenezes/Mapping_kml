# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:59:31 2020

@author: Rafael G. de Menezes
Oceanógrafo, Msc. Biotecnologia Marinha
Clube do Cientista
Biosustente Estudos Ambientais ltda.

Developed with Python 3.7.6

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
                   location and number of kilometers can be set at line 208
    SAVE FIGURE -> figure will be saved at the current working directory
                   default -> .png and 200 dpi
"""

class functions (): # functions to be used at main()

    def str_error (x): 
        # do not accept input (x) if it is not a number
        try:
            x = int(x)
        except:
            x = input('\nPlease enter a NUMBER:\n  ')
        return x

    def number_error (min, max): 
        # do not accept input if its value is not in aceptable range (between min and max args)
        x = input('\nEnter the corresponding NUMBER:\n  ')
        while type(x) == str:
            x = functions.str_error(x)
        while x not in range(min,max):
            x = input('\nINVALID number, please type again:\n  ')
            x = functions.str_error(x)
        return x
    
    def kmlbase_selection ():
        # user interaction to define kml base (folder) to use
        import os        
        kml_options = next(os.walk('.'))[1]
        if 'kmlbase' in kml_options:
            os.chdir('kmlbase')           
            kml_options = next(os.walk('.'))[1]
        
        print ('\n\n ------------- Mapping_kml -------------\n')
        print ('Which .kml database to plot?\n')
        for i in range(1, len(kml_options) + 1):
            print (i,' = ',kml_options[i - 1])
        print ('\nREMEMBER: if your kmlbase is not in the list, it is not properly located.')
        n = functions.number_error (1, len(kml_options) + 1)
        n = n - 1
        print('\nDatabase chosen: ',kml_options[n])       
        os.chdir(kml_options[n])
        return (kml_options[n])

    def baselayer_plot(ax, self, name): # plot kml files
        # ax   = object to receive the plot
        # self = pd.DataFrame with the coords to plot
        # name = kml base (folder) choose
               
        kml_list  = self.drop_duplicates('Filename')['Filename'].reset_index (drop = True)
        for n in kml_list:
            if n[:3] == 'bat':
                ax.plot(self['Lon'][self['Filename'] == n], self['Lat'][self['Filename'] == n],'-k', linewidth=0.8, alpha=0.6)
            else:
                ax.plot(self['Lon'][self['Filename'] == n], self['Lat'][self['Filename'] == n],'k')                
                ax.fill(self['Lon'][self['Filename'] == n], self['Lat'][self['Filename'] == n], 'gray', alpha=0.4)
        ax.axis('scaled')
        if name == 'Arraial do Cabo':
            ax.set_xlim(-42.054,-41.96)
            ax.set_ylim(-23.04,-22.938)
        elif name == 'Fernando de Noronha':
            ax.set_xlim(-32.50,-32.35)
            ax.set_ylim(-3.92, -3.79) 
        # you can add other 'elif' conditions here to best fit your map
        from matplotlib.ticker import FormatStrFormatter
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        return ax
    
    def baselayer_labels(ax, name, language = 'pt', font=12):
        # set axis labels and others examples customized labels
        # ax       = object to receive the plot
        # name     = kml base (folder) choose
        # language = options (english or portuguese) to example labels (default = pt)
        # font     = font size

        if name == 'Arraial do Cabo':
            name_loc  = (-42.0367,-22.965)
            bat_x     = -42.0528
            #ax.annotate('5 m',(bat_x,-22.9628),fontsize=font-6)
            #ax.annotate('10 m',(bat_x,-22.9658),fontsize=font-6)    
            ax.annotate('50 m',(bat_x,-22.99),fontsize=font-6)
            ax.annotate(name,name_loc, fontsize=font-2)        
            if language == 'pt':
                ax.annotate('Ilha do Cabo Frio',(-42.0016,-22.9968), fontsize=font-2)
                ax.annotate('Oceano Atlântico',(-42,-23.032), fontsize=font)
            elif language == 'en':
                ax.annotate('Cabo Frio Island',(-41.9960,-22.9968), fontsize=font-2)
                ax.annotate('Atlantic Ocean',(-41.9769,-23.0237), fontsize=font)    
    
        elif name == 'Fernando de Noronha':
            name_loc  = (-32.438, -3.8545)
            bat_y     = -3.87
            xy_bat5   = (-32.477, bat_y - 0.002)
            xy_bat50  = (-32.4902, bat_y)
            xy_ocean  = (-32.49, -3.90)
            if language == 'pt':
                name_ocean = 'Oceano Atlântico'
            elif language == 'en':
                name_ocean = 'Atlantic Ocean'
            ax.annotate(name,name_loc, fontsize=font-2)        
            ax.annotate(name_ocean, xy_ocean, fontsize=font)    
            ax.annotate('5 m', xy_bat5, fontsize = font - 6)
            ax.annotate('50 m', xy_bat50, fontsize = font - 6)
                   
        ax.set_ylabel('Latitude (ºS)', labelpad=25, fontsize=font)
        ax.set_xlabel('Longitude (ºW)', labelpad=25, fontsize=font)
        return ax

    def scale(ax, n = 0, loc = 'dl', font = 10):  
        # plot scale, in kilometers (km), and North arrow
        # n    = number of kilometers on scale (0 = auto)
        # loc  = location of scale and North arrow (default = down left)
        # font = font size
        
        import matplotlib.pyplot as plt
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        x = (xlim[1]-xlim[0])/10
        y = (ylim[1]-ylim[0])/10
        
        # defining scale position
        if loc   == 'dl': # down left
            xy   = [xlim[0] + x, ylim[0] + y]
        elif loc == 'dr': # down right
            xy   = [xlim[1] - 2*x, ylim[0] + y]         
        elif loc == 'ul': # upper left
            xy   = [xlim[0] + x, ylim[1] - 2*y]  
        elif loc == 'ur': # upper right
            xy   = [xlim[1] - 1.5*x, ylim[1] - 1.5*y]   
            
        # defining scale length    
        d = ((x+y)/2) # axis scale factor , in degrees
        if n == 0:
            km_n = int(d*60*1.852) # scale factor to kilometers
        else:
            km_n = n
            
        # scale horizontal line
        x1   = [xy[0], xy[0] + d]
        y1   = [xy[1], xy[1]]             
        lin1 = plt.Line2D(x1, y1, color = 'black', label = '_nolegend_')
        ax.add_line(lin1)
        # scale vertical line (left side)
        x2   = [x1[0], x1[0]]
        y2   = [y1[0] - d / 4, y1[0] + d / 4]
        ax.plot(x2, y2, color = 'black', label='_nolegend_')
        
        # scale size text
        ax.annotate(str(km_n) +' km', (x1[0] + d/10, y1[0] - d/2.5), fontsize = font)
        # North arrow and text
        ax.arrow(x1[0] + d/2, y1[0] + d/3, 0, d/3, width = d/12, head_width = d/4, color = 'k')
        ax.annotate('N', (x1[0] + d/2.5, y1[0] + 1.2*d), fontsize = font+4)
     
        
def main (figsize = (8,8), fmt = '.png', dpi = 200):
    # main mapping flow
    import os
    path = os.getcwd()
    if path.split('\\')[-1] != 'Mapping_kml':
        os.chdir('Mapping_kml')
    from kml_to_df import kml_to_df     
    selected_base = functions.kmlbase_selection()
    coords_df = kml_to_df()
    os.chdir(path)
        
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=figsize)    # creating figure
    ax  = plt.subplot2grid((1,1), (0,0)) # creating axes
        
    ax = functions.baselayer_plot(ax, coords_df, selected_base)
    ax = functions.baselayer_labels(ax, selected_base, 'pt', 12)
    if selected_base == 'Fernando de Noronha':
        functions.scale(ax, loc = 'ul')
    else: 
        functions.scale(ax)
    # just add other elif conditions to customize for other kmlbase
    from datetime import datetime as dt
    hora = dt.now().strftime('%d_%m_%Y_%H_%M')
    fig.savefig ('kmlMap_'+selected_base+'_'+hora+fmt, dpi= dpi)
    fig.show()    
    
if __name__ == "__main__":
    main()