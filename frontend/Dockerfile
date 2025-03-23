FROM node:18-alpine AS build

WORKDIR /app
COPY . .
RUN find ./ -type f 
RUN npm install
RUN npm run build

EXPOSE 3000

CMD ["node", "build/index.js"]
