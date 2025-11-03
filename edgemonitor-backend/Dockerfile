# Use Maven to build the app
FROM maven:3.9.11-eclipse-temurin-24 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src

# Run tests
RUN mvn test

# Package app (skip tests because they already ran)
RUN mvn clean package -DskipTests

# Package app with JDK
FROM eclipse-temurin:24-jdk AS runtime
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]