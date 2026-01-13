#!/bin/bash
# Script de compilación para Linux/Mac
# Uso: ./compile.sh

echo "Compilando documento LaTeX..."
echo ""

echo "Primera pasada..."
pdflatex -interaction=nonstopmode documento_proyecto.tex

echo ""
echo "Segunda pasada (para referencias cruzadas)..."
pdflatex -interaction=nonstopmode documento_proyecto.tex

echo ""
echo "Limpiando archivos auxiliares..."
rm -f *.aux *.log *.out *.toc

echo ""
echo "Compilación completada!"
echo "El archivo documento_proyecto.pdf está listo."
echo ""

# Abrir el PDF automáticamente (Linux/Mac)
if [ -f documento_proyecto.pdf ]; then
    if command -v xdg-open > /dev/null; then
        xdg-open documento_proyecto.pdf
    elif command -v open > /dev/null; then
        open documento_proyecto.pdf
    fi
fi

