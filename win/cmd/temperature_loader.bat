@echo off
cd /d %~dp0
if not "%X_MIMIMIZED%"=="1" (
	set X_MIMIMIZED=1
	start /min cmd /c,"%~0" %*
	exit
)
call C:\\ProgramData\\Anaconda3\\Scripts\\activate.bat
call activate weather
pythonw "%MYAPPS_PATH%\Temperature Loader.py"