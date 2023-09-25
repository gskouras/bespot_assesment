# Use the official Node.js image
FROM node:20

# Set the working directory in the container
WORKDIR /app/

RUN npm install -g npm@10.1.0

# Copy package.json and package-lock.json to the container
COPY ./web_application/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY ./web_application .
# Specify the command to run your application

CMD ["npm", "start", "dev:watch"]
