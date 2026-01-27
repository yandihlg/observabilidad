# Stage 1: Build
FROM maven:3.9.6-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy pom.xml
COPY pom.xml .

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:21-jre

WORKDIR /app

# Download OpenTelemetry Java Agent
RUN apt-get update && apt-get install -y wget && \
    wget -q https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v2.4.0/opentelemetry-javaagent.jar && \
    chmod +x opentelemetry-javaagent.jar && \
    apt-get remove -y wget && \
    apt-get clean

# Copy the JAR from the builder stage
COPY --from=builder /app/target/*.jar app.jar

# Set OpenTelemetry Environment Variables
ENV OTEL_JAVAAGENT_ENABLED=true
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_LOGS_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
ENV OTEL_SERVICE_NAME=customer-api
ENV OTEL_TRACES_SAMPLER=always_on
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

# Expose port
EXPOSE 8080

# Run the application with OpenTelemetry agent
ENTRYPOINT ["java", "-javaagent:./opentelemetry-javaagent.jar", "-jar", "app.jar"]
