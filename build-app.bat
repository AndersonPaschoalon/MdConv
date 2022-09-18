call Env/Scripts/activate.bat

echo Generating requirements.txt file...
pip freeze > requirements.txt

echo Building project
python -m PyInstaller --clean --onefile --icon=.\resources\markdown_here_ico.ico --collect-all reportlab.graphics.barcode  Main.py

echo Renaming binary file
move dist\Main.exe dist\mdconv.exe

echo Executing tests
robocopy dist\ tests\  "mdconv.exe" /z
pushd .\tests\
python run-tests.py
popd

