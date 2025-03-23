FROM node:18-alpine AS build

WORKDIR /
COPY . .
RUN npm install
RUN npm run build

EXPOSE 3000

CMD ["node", "build/index.js"]
