# Taking a parent image of jdk-17
FROM amazoncorretto:17-al2023-jdk

# Set working directory
WORKDIR /app

# Copy the jar file to new path
COPY target/code-quality-analyzer-backend-0.0.1-SNAPSHOT.jar /app/app.jar

# Exposing the port of Spring Boot Application
EXPOSE 8080

# Run the Spring Boot App
ENTRYPOINT ["java", "-jar", "app.jar"]