# Use a lightweight Java 17 runtime
FROM openjdk:17-jdk-slim

# Set working directory
WORKDIR /app

# Copy the jar file into the image
COPY target/*.jar app.jar

# Expose port 8080 (Spring Boot default)
EXPOSE 8080

# Run the jar
ENTRYPOINT ["java", "-jar", "app.jar"]