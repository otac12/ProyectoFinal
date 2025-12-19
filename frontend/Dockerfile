FROM node:18-alpine

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 3000

# Iniciar aplicación
CMD ["npm", "start"]

