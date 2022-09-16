call Env/Scripts/activate.bat

echo Generating requirements.txt file...
pip freeze > requirements.txt

echo Building project
python -m PyInstaller --onefile --icon=.\Resources\ii.ico --collect-all reportlab.graphics.barcode  Main.py

echo Renaming binary file
move dist\Main.exe dist\mdconv.exe