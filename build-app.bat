call Env/Scripts/activate.bat

echo Generating requirements.txt file...
pip freeze > requirements.txt

echo Building project
python -m PyInstaller --onefile --icon=.\resources\markdown_here_logo_icon_169967.ico --collect-all reportlab.graphics.barcode  Main.py

echo Renaming binary file
move dist\Main.exe dist\mdconv.exe

echo Executing tests
cp dist\mdconv.exe tests\mdconv.exe
pushd .\tests\
python run-tests.py
popd

