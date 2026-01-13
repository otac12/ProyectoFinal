# Instrucciones para usar en Overleaf (LaTeX Web)

## Pasos para importar el documento a Overleaf

### Opción 1: Subir archivo directamente

1. Ve a [Overleaf](https://www.overleaf.com/) e inicia sesión
2. Crea un nuevo proyecto o abre uno existente
3. Haz clic en el botón **"Upload"** (Subir) en la barra superior
4. Selecciona el archivo `documento_proyecto.tex`
5. Espera a que se suba y compile automáticamente

### Opción 2: Copiar y pegar el contenido

1. Abre `documento_proyecto.tex` en tu editor
2. Selecciona todo el contenido (Ctrl+A / Cmd+A)
3. Copia el contenido (Ctrl+C / Cmd+C)
4. En Overleaf, crea un nuevo proyecto con plantilla "Blank Project"
5. Elimina el contenido del archivo `main.tex` (o crea un nuevo archivo)
6. Pega todo el contenido (Ctrl+V / Cmd+V)
7. Guarda el archivo (Ctrl+S / Cmd+S)
8. Overleaf compilará automáticamente

## Configuración del Compilador

En Overleaf, asegúrate de usar:

- **Compiler**: `pdfLaTeX`
- **Main document**: `documento_proyecto.tex` (o el nombre que hayas dado)

Para cambiar el compilador:
1. Ve al menú superior
2. Click en el menú donde dice "Menu"
3. Selecciona "Compiler" → "pdfLaTeX"

## Paquetes Necesarios

Todos los paquetes usados están disponibles en Overleaf por defecto:
- ✅ babel (con soporte para español)
- ✅ tikz y pgfplots
- ✅ listings
- ✅ hyperref
- ✅ amsmath
- ✅ booktabs
- ✅ longtable

**No necesitas instalar nada adicional** - Overleaf ya tiene todos los paquetes.

## Solución de Problemas

### Error: "Missing \end{document}"

- Asegúrate de que el documento tenga `\begin{document}` y `\end{document}`
- Verifica que no hayas copiado solo una parte del documento

### Error: "Undefined control sequence"

- Verifica que todos los paquetes estén cargados correctamente
- Asegúrate de que el compilador sea `pdfLaTeX` (no XeLaTeX o LuaLaTeX)

### Los diagramas no se muestran

- Espera unos segundos más, TikZ puede tardar en compilar diagramas complejos
- Si persiste, intenta recompilar haciendo clic en "Recompile"

### Referencias cruzadas no funcionan

- Compila el documento dos veces (Overleaf normalmente lo hace automáticamente)
- Si no, haz clic en "Recompile" una segunda vez

### Caracteres especiales en español

- El documento usa `\usepackage[utf8]{inputenc}` y `\usepackage[spanish]{babel}`
- No debería haber problemas con acentos o ñ
- Si ves caracteres raros, verifica que la codificación del archivo sea UTF-8

## Consejos para Overleaf

1. **Auto-compilación**: Overleaf compila automáticamente cuando guardas cambios
2. **Vista dividida**: Puedes ver el código LaTeX y el PDF lado a lado
3. **Historial**: Overleaf guarda un historial de versiones (menú "History")
4. **Colaboración**: Puedes compartir el proyecto con otros usuarios
5. **Sincronización**: Conecta Overleaf con Git para sincronizar con tu repositorio

## Exportar el PDF

Una vez compilado correctamente:

1. Haz clic en el botón **"Download PDF"** (arriba a la izquierda)
2. O usa el menú → "Download" → "PDF"

## Compartir el Documento

Para compartir el proyecto en Overleaf:

1. Ve al menú superior
2. Click en "Share"
3. Copia el enlace o invita a colaboradores por email

## Notas Importantes

- ✅ El documento está optimizado para Overleaf
- ✅ Todos los diagramas TikZ están incluidos
- ✅ No necesitas archivos adicionales
- ✅ Todo está en un solo archivo `.tex`

## Estructura del Proyecto en Overleaf

Después de subir, deberías ver:
```
Proyecto/
└── documento_proyecto.tex  (archivo principal)
```

Si quieres organizarlo mejor, puedes crear carpetas:
```
Proyecto/
├── main.tex              (copia del documento)
└── images/               (si necesitas imágenes externas)
```

Pero **NO es necesario** - el documento actual funciona completamente sin archivos adicionales.

