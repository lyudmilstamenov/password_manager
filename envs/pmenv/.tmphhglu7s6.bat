@ECHO OFF
@SET PYTHONIOENCODING=utf-8
@SET PYTHONUTF8=1
@FOR /F "tokens=2 delims=:." %%A in ('chcp') do for %%B in (%%A) do set "_CONDA_OLD_CHCP=%%B"
@chcp 65001 > NUL
@CALL "C:\Users\ASUS\anaconda3\condabin\conda.bat" activate "E:\FMI\4 year\7 term\Python\project\password_manager\envs\pmenv"
@IF %ERRORLEVEL% NEQ 0 EXIT /b %ERRORLEVEL%
@"E:\FMI\4 year\7 term\Python\project\password_manager\envs\pmenv\python.exe" -Wi -m compileall -q -l -i C:\Users\ASUS\AppData\Local\Temp\tmpadyicgg1 -j 0
@IF %ERRORLEVEL% NEQ 0 EXIT /b %ERRORLEVEL%
@chcp %_CONDA_OLD_CHCP%>NUL
