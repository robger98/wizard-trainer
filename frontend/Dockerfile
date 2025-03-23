FROM node:18-alpine AS build

WORKDIR /app
COPY . .
RUN dir -s
RUN npm install
RUN npm run build

EXPOSE 3000

CMD ["node", "build/index.js"]
