# Etapa de Build: utiliza uma imagem Node para instalar dependências e compilar a aplicação
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Etapa de execução: utiliza uma imagem Node leve para rodar a aplicação compilada
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm", "run", "start"]