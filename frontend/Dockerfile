# Use the official Node.js image as the base image
FROM node:20.10.0-alpine AS build

# Set the working directory
WORKDIR /frontend

# Copy vue/package.json and vue/package-lock.json
COPY vue/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY ./vue .

# Build the Vue.js application
RUN npm run build

# Use the official Nginx image to serve the application
FROM nginx:alpine

# Copy the built application from the previous stage
COPY --from=build /frontend/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]