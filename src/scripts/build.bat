REM rmdir /S dist
REM rmdir /S build

copy package\DV.spec

C:\Python27\Scripts\pyinstaller.exe DV.spec

copy dist\DBUpdater\*.* dist\Server

md App\package\Server

xcopy /E dist\Server\*.* App\package\Server
copy package\install_win.bat App\
copy README.txt App\

