@echo off
set pyfiles_ROOT=%~dp0
set XGISBASE=%pyfiles_ROOT%
REM set GISDBASE=C:\Users\Administrator\Documents\GitHub\wp07-lulc-w32\GRASS_data
REM set GISRC=%~dp0.grassrc6
set OSGEO4W_ROOT=C:\OSGeo4W64
set GISBASE=%OSGEO4W_ROOT%\apps\grass\grass-6.4.3
set Landsat_LDOPE=C:\Program Files\Landsat_LDOPE\windows64bit_bin
set Landsat_download=C:\Users\Administrator\Documents\GitHub\LANDSAT-Download
set starspan=C:\Program Files\starspan
REM set GRASS7=C:\Program Files (x86)\GRASS GIS 7.0.0beta2\lib
set LD_LIBRARY_PATH=%GISBASE%\lib
set PYTHON=%OSGEO4W_ROOT%\apps\python27
set DWEISPYTHONLIBS=%XGISBASE%\etc\python
set OSGEO4W=%OSGEO4W_ROOT%\bin
set OSGEO4W_ETC=%OSGEO4W_ROOT%\etc\ini
set GRASSBIN=%GISBASE%\bin
set GDAL_DATA=%pyfiles_ROOT%gdal
set osgeo_python=%OSGEO4W_ROOT%\apps\python27
set osgeo_python_scripts=%OSGEO4W_ROOT%\apps\python27\Scripts
set OTB=%OSGEO4W_ROOT%\apps\orfeotoolbox\python
set LIB=%pyfiles_ROOT%lib
set EXTLIB=%pyfiles_ROOT%extlib
set MSYS=%OSGEO4W_ROOT%\apps\msys\bin
set GRASS_SH=%OSGEO4W_ROOT%\apps\msys\bin\sh.exe

PATH=%LIB%;%EXTLIB%;%osgeo_python%;%osgeo_python_scripts%;%OSGEO4W%;%OSGEO4W_ETC%;%Landsat_LDOPE%;%Landsat_download%;%GRASSBIN%;%LD_LIBRARY_PATH%;%starspan%;%MSYS%
set PYTHONPATH=%DWEISPYTHONLIBS%;%OTB%;%LIB%
