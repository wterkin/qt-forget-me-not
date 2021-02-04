rem conda activate PyQt5
rem d:
rem cd D:\home\projects\python\qt_forget_me_not_dist
rem echo y | del *.*
C:\Languages\anaconda3\envs\PyQt5\Scripts\pyinstaller.exe --onedir --hidden-import "PyQt5" --hidden-import "PyQt5" --hidden-import "QtWidgets" --distpath ..\qt_forget_me_not_dist\ --workpath D:\temp\ --clean --noupx -y --log-level WARN --name forget-me-not -i ui\forget-me-not.ico main.py 2>compile.log
rem -w - без консоли
rem conda deactivate
rem --hidden-import "PyQt5" --hidden-import "PyQt5" --hidden-import "QtWidgets"
pause