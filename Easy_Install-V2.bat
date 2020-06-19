@echo off
pushd "%~dp0"

echo.
echo  :: Checking For Administrator Elevation...
echo.
timeout /t 1 /nobreak > NUL
openfiles > NUL 2>&1
if %errorlevel%==0 (
        echo Elevation found! Proceeding...
) else (
        echo  :: You are NOT running as Administrator
        echo.
        echo     Right-click and select ^'Run as Administrator^' and try again.
        echo     Press any key to exit...
        pause > NUL
        exit
)

set PATH=%PATH%;%PROGRAMDATA%\chocolatey\lib\adb\tools\platform-tools\;%PROGRAMFILES%\Git\cmd;%PROGRAMDATA%\chocolatey\bin

goto menu

:menu
	cls
	echo.
	echo  :: Easy install for ALAS
	echo. 
	echo  This script will install Python 3.7.6 + requirements.txt + ADB + GIT + CHOCOLATEY
	echo. 
	echo  :: By whoamikyo
	echo. 
	echo     1. Essentials programs
	echo     2. Clone repository
	echo     3. Python 3.7.6 + requirements.txt
	echo     4. Updater Only
	echo.
	echo			Install in order
	echo. 
	echo  :: Type a 'number' and press ENTER
	echo  :: Type 'exit' to quit
	echo.
	
	set /P menu=
		if %menu%==1 GOTO programs
		if %menu%==2 GOTO clone
		if %menu%==3 GOTO python
		if %menu%==4 GOTO updater
		if %menu%==exit GOTO EOF
		
		else (
		cls
	echo.
	echo  :: Incorrect Input Entered
	echo.
	echo     Please type a 'number' or 'exit'
	echo     Press any key to return to the menu...
	echo.
		pause > NUL
		goto menu
		)
		

:programs
cls
	echo.
	echo  :: Checking For Internet Connection...
	echo.
	timeout /t 2 /nobreak > NUL

	ping -n 1 archlinux.org -w 20000 >nul

	if %errorlevel% == 0 (
	echo Internet Connection Found! Proceeding...
	) else (
		echo  :: You are NOT connected to the Internet
		echo.
        echo     Please enable your Networking adapter and connect to try again.
        echo     Press any key to retry...
        pause > NUL
        goto packages
	)
		cls
		echo.
		echo  :: Installing Packages...
		echo.
		timeout /t 1 /nobreak > NUL
				
		@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin

		@powershell -NoProfile -ExecutionPolicy Bypass -Command "choco install -y --force --allow-empty-checksums adb git"

:: timout
PowerShell -Command "Start-Sleep -s 10" > nul 2>&1
:: killing adb server
call adb kill-server > nul 2>&1

goto menu

:clone
echo Cloning repository
git clone https://github.com/LmeSzinc/AzurLaneAutoScript.git && cd AzurLaneAutoScript && git remote add whoamikyo https://github.com/whoamikyo/AzurLaneAutoScript.git

goto menu

:python
cls
echo.
echo  :: Installing Python 3.7.6 + requirements.txt
echo.
echo.
set ROOT=%~dp0AzurLaneAutoScript
set FILE_URL="https://gitlab.com/whoamikyo/alas-venv/-/raw/master/python.zip"
set FILE_DEST=%ROOT%\pythonpackage.zip
if not exist %ROOT% (
  mkdir %ROOT%
)
 if not exist "%FILE_DEST%" (
   echo Downloading with powershell: %FILE_URL% to %FILE_DEST%
   powershell.exe -command "$webclient = New-Object System.Net.WebClient; $url = \"%FILE_URL%\"; $file = \"%FILE_DEST%\"; $webclient.DownloadFile($url,$file);"
   echo Expanding with powershell to: %ROOT%
   powershell -command "$shell_app=new-object -com shell.application; $zip_file = $shell_app.namespace(\"%FILE_DEST%\"); $destination = $shell_app.namespace(\"%ROOT%\"); $destination.Copyhere($zip_file.items())"
 ) else (
   echo "pythonpackage.zip already downloaded, delete to re-download"
 )

goto menu

:updater
	cls
	echo.
	echo  :: This update only will work if you downloaded ALAS with this file using option 2. clone
	echo. 
	echo	::DISCLAIMER
	echo	IF YOU GET THE FOLLOWING ERROR: 
	echo	"error: Your local changes to the following files would be overwritten by merge:Easy_Install-V2.bat"
	echo	YOU NEED RE-DOWNLOAD ONLY Easy_Install-V2.bat FILE FROM REPOSITORY AND OVERWRITTEN THE OLD FOR NEW FILE	
	echo. 
	echo     1. https://github.com/LmeSzinc/AzurLaneAutoScript (Main Repo, When in doubt, use it)
	echo     2. https://github.com/whoamikyo/AzurLaneAutoScript (Mirrored Fork)
	echo     3. https://github.com/whoamikyo/AzurLaneAutoScript (nightly build, dont use)
	echo     4. Back to main menu
	echo. 
	echo  :: Type a 'number' and press ENTER
	echo  :: Type 'exit' to quit
	echo.
	
	set /P choice=
		if %choice%==1 GOTO LmeSzinc
		if %choice%==2 GOTO whoamikyo
		if %choice%==3 GOTO nightly
		if %choice%==4 GOTO menu
		if %choice%==exit GOTO EOF
		
		else (
		cls
	echo.
	echo  :: Incorrect Input Entered
	echo.
	echo     Please type a 'number' or 'exit'
	echo     Press any key to return to the menu...
	echo.
		pause > NUL
		goto updater
		)
		

:LmeSzinc
git fetch origin master && git reset --hard origin/master && git pull --ff-only origin master
:: timout
PowerShell -Command "Start-Sleep -s 10" > nul 2>&1
goto updater
:whoamikyo
git fetch whoamikyo master && git reset --hard whoamikyo/master && git pull --ff-only whoamikyo master
:: timout
PowerShell -Command "Start-Sleep -s 10" > nul 2>&1
goto updater
:nightly
git fetch whoamikyo nightly && git reset --hard whoamikyo/nightly && git pull --ff-only whoamikyo nightly
:: timout
PowerShell -Command "Start-Sleep -s 10" > nul 2>&1
goto updater