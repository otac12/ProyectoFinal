# Simulador de Red FTTH GPON

Sistema completo para simular, planificar y analizar redes de fibra óptica FTTH (Fiber To The Home) usando tecnología GPON.

## Requisitos Previos

- Docker Desktop instalado y ejecutándose
- Docker Compose (incluido en Docker Desktop)
- Al menos 4GB de RAM disponibles
- Puertos disponibles: 3001 (frontend), 5000 (backend), 3306 (MySQL)

## Instalación y Ejecución

### Paso 1: Clonar o descargar el proyecto

Si tienes el código en un repositorio:
```bash
git clone <url-del-repositorio>
cd Proyecto
```

### Paso 2: Iniciar los servicios con Docker Compose

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
docker-compose up --build
```

Este comando:
- Construye las imágenes de Docker para backend y frontend
- Descarga la imagen de MySQL
- Inicia los tres servicios (MySQL, backend, frontend)
- Configura la base de datos automáticamente

**Nota:** La primera vez puede tardar varios minutos mientras descarga e instala las dependencias.

### Paso 3: Verificar que todo esté funcionando

Espera a ver estos mensajes en la terminal:

```
ftth_mysql    | ... ready for connections
ftth_backend  | * Running on all addresses (0.0.0.0)
ftth_frontend | Compiled successfully!
```

### Paso 4: Acceder a la aplicación

Abre tu navegador web y ve a:

```
http://localhost:3001
```

Deberías ver la interfaz del simulador.

## Uso de la Aplicación

### 1. Crear una Topología de Red

1. Ve a la pestaña **"Gestión de Topologías"**
2. Completa el formulario:
   - **Nombre:** Nombre descriptivo para tu red
   - **Descripción:** (Opcional) Descripción de la topología
   - **Número de ONUs:** Cantidad de dispositivos finales (1-128)
   - **Ratio de Splitter:** Relación de división óptica (1:8, 1:16, 1:32, 1:64)
3. Haz clic en **"Crear Topología"**
4. La nueva topología aparecerá en la lista del lado derecho

### 2. Visualizar el Diagrama de Red

1. Selecciona una topología de la lista haciendo clic en ella
2. Ve a la pestaña **"Diagrama de Red"**
3. Verás una representación visual de tu red GPON:
   - **Azul:** OLT (Terminal de línea óptica)
   - **Naranja:** Splitter óptico
   - **Verde:** ONUs (Unidades de red óptica)
   - **Líneas:** Conexiones de fibra óptica
4. Usa los controles del diagrama para:
   - Hacer zoom con la rueda del mouse
   - Arrastrar nodos para reorganizar
   - Ver el minimapa en la esquina inferior izquierda

### 3. Ejecutar una Simulación

1. Asegúrate de tener una topología seleccionada
2. Ve a la pestaña **"Simulación"**
3. Completa los parámetros:
   - **Nombre de la Simulación:** Identificador para los resultados
   - **Tiempo de Simulación:** Duración en segundos (ej: 100)
4. Haz clic en **"Ejecutar Simulación"**
5. Espera a que termine (verás un indicador de progreso)

### 4. Ver Resultados

1. Después de ejecutar la simulación, automáticamente se abrirá la pestaña **"Resultados"**
2. Verás:
   - **Resumen General:** Métricas agregadas
   - **Gráficos de Throughput:** Ancho de banda por ONU
   - **Gráficos de Paquetes:** Paquetes enviados por ONU
   - **Tabla Detallada:** Todas las métricas individuales

## Detener la Aplicación

Para detener todos los servicios, presiona `Ctrl+C` en la terminal donde está corriendo Docker Compose, o ejecuta:

```bash
docker-compose down
```

Para detener y eliminar también los volúmenes (incluyendo la base de datos):

```bash
docker-compose down -v
```

## Solución de Problemas

### El frontend no carga

- Verifica que el puerto 3001 no esté en uso
- Espera unos minutos después de `docker-compose up` para que compile React
- Revisa los logs: `docker-compose logs frontend`

### El backend no responde

- Verifica que MySQL esté corriendo: `docker-compose logs mysql`
- Revisa los logs del backend: `docker-compose logs backend`
- Asegúrate de que el puerto 5000 no esté ocupado

### Error de conexión a la base de datos

- Espera a que MySQL termine de inicializarse (puede tardar 30-60 segundos)
- Reinicia los servicios: `docker-compose restart`

### Ver logs de un servicio específico

```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql
```

### Reconstruir desde cero

Si algo no funciona, puedes limpiar todo y empezar de nuevo:

```bash
docker-compose down -v
docker-compose up --build
```

## Estructura del Proyecto

```
Proyecto/
├── docker-compose.yml          # Configuración de Docker
├── backend/                    # Aplicación Python Flask
│   ├── Dockerfile
│   ├── app.py                  # Servidor Flask principal
│   ├── requirements.txt
│   ├── models/                 # Clases de elementos de red
│   ├── simulators/             # Simuladores de tráfico y DBA
│   └── database/               # Scripts SQL
├── frontend/                   # Aplicación React
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── App.js
│       └── components/         # Componentes React
└── README.md                   # Este archivo
```

## Características Principales

- ✅ Creación de topologías GPON personalizables
- ✅ Visualización interactiva de redes con diagramas
- ✅ Simulación de tráfico Triple Play (video, internet, voz)
- ✅ Cálculo de power budget óptico
- ✅ Algoritmo DBA (Dynamic Bandwidth Allocation)
- ✅ Métricas de rendimiento en tiempo real
- ✅ Gráficos y visualizaciones de resultados
- ✅ Base de datos persistente para guardar configuraciones

## Notas Importantes

- Los datos se guardan en un volumen de Docker, así que aunque detengas los contenedores, las topologías y simulaciones se conservan
- Si eliminas el volumen (`docker-compose down -v`), se perderán todos los datos
- El frontend se compila automáticamente al iniciar, puede tardar 1-2 minutos la primera vez

## Soporte

Si encuentras problemas, revisa los logs con `docker-compose logs` o reinicia los servicios con `docker-compose restart`.

