# Taking a parent image of node 18
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json file and install dependencies
COPY package.json ./
RUN npm install --legacy-peer-deps

# Copy the build folder
COPY build ./build/

# Install the serve tool
RUN npm install -g serve

# Exposing the port of React Application
EXPOSE 3000

# Run the React App (Serve the Frontend build)
ENTRYPOINT ["serve", "-s", "build"]