@echo off
echo Wain until it's done
(
if exist c:\Python27\python.exe (
	set PythonBin=c:\Python27\python.exe
) else if exist c:\Python34\python.exe (
	set PythonBin=c:\Python34\python.exe
) else (
	echo "Cannot find Python"
	exit
)

"Robot-Framework\wxpython2.8.exe" /S /norestart

cd Robot-Framework\robotframework-3.0.1
rem start /wait python setup.py install
%PythonBin% setup.py install || GOTO ERROR_RF

cd ..\robotframework-ride-1.5.2.1
rem start /wait python setup.py install
%PythonBin% setup.py install || GOTO ERROR_RIDE

cd ..\PyMySQL-0.7.9
%PythonBin% setup.py install || GOTO ERROR_MySQL

cd ..\robotframework-databaselibrary-0.6
%PythonBin% setup.py install || GOTO ERROR_MySQL

cd ..\Excel\natsort-3.3.0
rem start /wait python setup.py install
%PythonBin% setup.py install || GOTO ERROR_Excel
cd ..\NaviNet-robotframework-excellibrary-8744913
rem start /wait python setup.py install
%PythonBin% setup.py install || GOTO ERROR_Excel
cd ..\xlrd-1.0.0
rem start /wait python setup.py install
%PythonBin% setup.py install || GOTO ERROR_Excel
cd ..\xlutils-1.7.1
rem start /wait python setup.py install
%PythonBin% setup.py install || GOTO ERROR_Excel
cd ..\xlwt-1.2.0
rem start /wait python setup.py install
%PythonBin% setup.py install || GOTO ERROR_Excel
cd ..\..
GOTO NOERROR
)>log.txt 1>suc.txt 2>err.txt 
pause

:ERROR_RF
type %cd%\err.txt
echo "Something went wrong with Robot Framework."
echo "Install is incomplete."
pause
exit

:ERROR_RIDE
type %cd%\err.txt
echo "Something went wrong with RIDE."
echo "Install is incomplete."
pause
exit

:ERROR_Excel
type %cd%\err.txt
echo "Something went wrong with Excel dependency."
echo "Install is incomplete."
pause
exit

:ERROR_MySQL
type %cd%\err.txt
echo "Something went wrong with MySQL dependency."
echo "Install is incomplete."
pause
exit

:NOERROR
type %cd%\suc.txt
echo "Install is done."
pause
exit


