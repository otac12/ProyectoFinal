# Documentación del Proyecto FTTH GPON

Este directorio contiene la documentación completa del proyecto en formato LaTeX.

## Archivos

- `documento_proyecto.tex` - Documento principal LaTeX con toda la información del proyecto

## Requisitos para Compilar

Para compilar el documento LaTeX necesitas tener instalado:

- **TeXLive** (recomendado) o **MiKTeX**
- Paquetes LaTeX necesarios (incluidos en la mayoría de distribuciones modernas):
  - `tikz` y `pgfplots` (para diagramas)
  - `listings` (para código)
  - `booktabs` y `longtable` (para tablas)
  - `hyperref` (para enlaces)

## Compilación

### Windows (MiKTeX)

```bash
pdflatex documento_proyecto.tex
pdflatex documento_proyecto.tex  # Segunda pasada para referencias
```

### Linux/Mac (TeXLive)

```bash
pdflatex documento_proyecto.tex
pdflatex documento_proyecto.tex
```

### Compilación con Make

Si tienes `make` instalado:

```bash
make pdf
```

## Contenido del Documento

El documento incluye:

1. **Resumen Ejecutivo** - Visión general del proyecto
2. **Introducción** - Contexto tecnológico y objetivos
3. **Arquitectura del Sistema** - Diagramas y componentes
4. **Modelado de Elementos de Red** - OLT, ONU, Splitter, Fiber
5. **Explicación del Código** - Fragmentos comentados
6. **Diagramas de Topologías** - Visualizaciones TikZ
7. **Arquitectura de la Aplicación** - Diagramas UML
8. **Especificaciones Técnicas** - Tablas y parámetros
9. **Fórmulas y Cálculos** - Ecuaciones matemáticas
10. **Conclusiones** - Resultados y mejoras futuras
11. **Apéndices** - Instalación y glosario

## Diagramas Incluidos

- Arquitectura de tres capas
- Topología en estrella (Star)
- Topología en árbol (Tree)
- Flujo de datos en GPON
- Diagrama de clases
- Flujo de datos en la API

## Tablas Incluidas

- Características del OLT
- Características de la ONU
- Pérdidas por Splitting
- Parámetros de Fibra Óptica
- Requisitos del Sistema
- Endpoints de la API
- Modelo de Base de Datos

## Notas

- El documento está en español
- Usa codificación UTF-8
- Los diagramas se generan automáticamente con TikZ
- El código fuente está resaltado con `listings`

## Solución de Problemas

Si encuentras errores al compilar:

1. **Paquetes faltantes**: Instala los paquetes necesarios con tu gestor de paquetes LaTeX
2. **Diagramas no se muestran**: Asegúrate de tener TikZ y PGFPlots instalados
3. **Referencias cruzadas**: Ejecuta `pdflatex` dos veces seguidas

## Generación Automática

Para automatizar la compilación, puedes usar el siguiente script:

### Windows (batch)
```batch
@echo off
pdflatex documento_proyecto.tex
pdflatex documento_proyecto.tex
del *.aux *.log *.out *.toc
```

### Linux/Mac (bash)
```bash
#!/bin/bash
pdflatex documento_proyecto.tex
pdflatex documento_proyecto.tex
rm -f *.aux *.log *.out *.toc
```

