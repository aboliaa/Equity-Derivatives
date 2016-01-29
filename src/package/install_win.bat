IF EXIST C:\AppHome GOTO ERROR
md C:\AppHome\bhavcopies
GOTO SUCCESS

:ERROR
echo Error in installation
GOTO :end

:SUCCESS
echo Installtion successful
