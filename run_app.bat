@echo off
cd /d "%~dp0"
echo Iniciando Streamlit desde: %cd%
poetry run streamlit run streamlits/app.py
pause

