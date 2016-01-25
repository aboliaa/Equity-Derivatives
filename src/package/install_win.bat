IF EXIST C:\DerivativesHome GOTO ERROR
md C:\DerivativesHome\bhavcopies
mklink 
GOTO SUCCESS

:ERROR
echo Error in installation
GOTO :end

:SUCCESS
echo Installtion successful
