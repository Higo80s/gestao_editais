@echo off
echo Atualizando dependências...
call .venv\Scripts\activate.bat
pip install ttkthemes python-dateutil pyinstaller openpyxl reportlab

echo Gerando executável...
 pyinstaller --onefile --windowed --name "GestaoEditais" --icon "icon.ico" app.py
echo.
echo ✅ CONCLUÍDO!
echo Executável em: dist\GestaoEditais.exe
 echo.
 echo IMPORTANTE: O banco de dados (gestao_editais.db) deve estar no mesmo
 echo diretório do executável para que os dados sejam salvos corretamente!
pause