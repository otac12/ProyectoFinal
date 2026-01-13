# Makefile para compilar el documento LaTeX
# Uso: make pdf

TEXFILE = documento_proyecto.tex
PDFFILE = documento_proyecto.pdf
AUXFILES = *.aux *.log *.out *.toc *.lof *.lot

# Compilador LaTeX
LATEX = pdflatex
LATEX_FLAGS = -interaction=nonstopmode

.PHONY: pdf clean view help

# Compilar el PDF
pdf: $(PDFFILE)

$(PDFFILE): $(TEXFILE)
	@echo "Compilando LaTeX (primera pasada)..."
	$(LATEX) $(LATEX_FLAGS) $(TEXFILE)
	@echo "Compilando LaTeX (segunda pasada para referencias)..."
	$(LATEX) $(LATEX_FLAGS) $(TEXFILE)
	@echo "Compilación completada: $(PDFFILE)"

# Limpiar archivos auxiliares
clean:
	@echo "Limpiando archivos auxiliares..."
	rm -f $(AUXFILES)
	@echo "Limpieza completada"

# Limpiar todo (incluido PDF)
clean-all: clean
	rm -f $(PDFFILE)

# Ver el PDF (Linux/Mac)
view: pdf
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(PDFFILE); \
	elif command -v open > /dev/null; then \
		open $(PDFFILE); \
	else \
		echo "No se encontró un visor PDF. Abre $(PDFFILE) manualmente."; \
	fi

# Ver el PDF (Windows)
view-win: pdf
	@start $(PDFFILE)

# Ayuda
help:
	@echo "Makefile para compilar documento LaTeX"
	@echo ""
	@echo "Uso:"
	@echo "  make pdf      - Compilar el documento PDF"
	@echo "  make clean    - Eliminar archivos auxiliares"
	@echo "  make clean-all - Eliminar archivos auxiliares y PDF"
	@echo "  make view     - Compilar y abrir el PDF (Linux/Mac)"
	@echo "  make view-win - Compilar y abrir el PDF (Windows)"
	@echo "  make help     - Mostrar esta ayuda"

