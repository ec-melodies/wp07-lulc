@echo off
rem Root OSGEO4W home dir to the same directory this script exists in

rem Convert double backslashes to single
set OSGEO4W_ROOT=C:\OSGeo4W64
echo. & echo ___________________________________________________________
echo. & echo Desertification Indicators Services (WP7) for FP7 MELODIES.
echo. & echo Land Use Land Cover Changes
echo. & echo ___________________________________________________________

rem Add application-specific environment settings
for %%f in ("%OSGEO4W_ROOT%\etc\ini\*.bat") do call "%%f"

set pyfiles_ROOT=%~dp0
call "%pyfiles_ROOT%\ini_path.bat"
REM call "C:\OSGeo4W64\apps\grass\grass-6.4.3\etc\env.bat"
python %pyfiles_ROOT%bin\lulc_main.py
Pause
