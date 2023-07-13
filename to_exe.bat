pip install -r requirements.txt
pyinstaller --add-data ".env:." --onefile gui_main.pyw
