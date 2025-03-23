# Stage 1: Build the frontend application
FROM node:18-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./
# If using yarn, uncomment the next line and comment the npm install line
# COPY yarn.lock ./

# Install dependencies
RUN npm ci
# If using yarn, uncomment the next line and comment the npm ci line
# RUN yarn install --frozen-lockfile

# Copy the rest of the frontend code
COPY . .

# Build the application
RUN npm run build
# If using yarn, uncomment the next line and comment the npm run build line
# RUN yarn build

# Stage 2: Serve the app with nginx
FROM nginx:alpine

# Copy the built app from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
