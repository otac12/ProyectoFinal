@echo off
REM Script de compilación para Windows
REM Uso: compile.bat

echo Compilando documento LaTeX...
echo.

echo Primera pasada...
pdflatex -interaction=nonstopmode documento_proyecto.tex

echo.
echo Segunda pasada (para referencias cruzadas)...
pdflatex -interaction=nonstopmode documento_proyecto.tex

echo.
echo Limpiando archivos auxiliares...
del /Q *.aux *.log *.out *.toc 2>nul

echo.
echo Compilacion completada!
echo El archivo documento_proyecto.pdf esta listo.
echo.

REM Abrir el PDF automáticamente
if exist documento_proyecto.pdf (
    start documento_proyecto.pdf
)

