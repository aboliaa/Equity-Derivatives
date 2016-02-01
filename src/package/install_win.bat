IF EXIST C:\AppHome GOTO X
md C:\AppHome\bhavcopies

:X
copy package\Server\static\holidays.txt C:\AppHome

:SUCCESS
echo Installtion successful
