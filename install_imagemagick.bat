@echo off
echo Installing ImageMagick for Windows...

REM Check if Chocolatey is installed
where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Chocolatey package manager...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
)

REM Install ImageMagick
choco install imagemagick -y

REM Add to system PATH
setx /M PATH "%PATH%;C:\Program Files\ImageMagick-7.1.1-Q16"

echo ImageMagick installation complete. Please restart your terminal.
