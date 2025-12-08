@echo off
echo Atualizando dependências...
call .venv\Scripts\activate.bat
pip install ttkthemes python-dateutil pyinstaller openpyxl reportlab

echo Gerando executável...
pyinstaller --onefile --windowed --name "GestaoEditais" --add-data "gestao_editais.db;." app.py

echo.
echo ✅ CONCLUÍDO!
echo Executável em: dist\GestaoEditais.exe
pause