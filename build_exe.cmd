rem conda activate PyQt5
rem d:
rem cd D:\home\projects\python\qt_forget_me_not_dist
rem echo y | del *.*
C:\Languages\Python-3.10\envs\qt\Scripts\pyinstaller.exe %1 --onefile --paths C:\Languages\Python-3.10\envs\qt\Lib\site-packages\PyQt5\ --distpath ..\distributive\ --workpath D:\temp\ --clean --noupx -y --log-level WARN --name forget-me-not -i ui\forget-me-not.ico main.py 2>compile.log
rem -hidden-import "PyQt5" --hidden-import "PyQt5" --hidden-import "QtWidgets"
md F:\Projects\-production\_forget_me_not\distributive\ui
rem \forget-me-not\
copy F:\Projects\-production\_forget_me_not\ui F:\Projects\-production\_forget_me_not\distributive\ui
rem forget-me-not\ui
rem md D:\home\projects\python\distributive\forget-me-not\platforms
rem copy D:\home\projects\python\DLLs\platforms\* D:\home\projects\python\distributive\forget-me-not\platforms
rem copy D:\home\projects\python\DLLs\* D:\home\projects\python\distributive\forget-me-not\
start F:\Projects\-production\_forget_me_not\distributive\forget-me-not\forget-me-not.exe
rem -w - без консоли
rem conda deactivate
rem --hidden-import "PyQt5" --hidden-import "PyQt5" --hidden-import "QtWidgets"
rem pause