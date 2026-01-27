# Customer API - Documentación Completa v4.0

> **Última actualización:** Enero 2026  
> **Stack:** Spring Boot 3.2.0 + Java 21 + OpenTelemetry v2.4.0 + Observabilidad Completa

## 🚀 INICIO RÁPIDO

```bash
# Instalación y validación automática en 3 pasos
python3 setup_and_test.py
```

Este script hace **TODO automáticamente**:
✅ Levanta 10 contenedores Docker  
✅ Espera a que se inicialicen  
✅ Valida que estén funcionando  
✅ Ejecuta 5 pruebas de API  
✅ Genera logs estructurados  
✅ Muestra tablas con resultados  
✅ Proporciona URLs de acceso  

---

## 📋 Índice
1. [Inicio Rápido con Script Python](#inicio-rápido)
2. [Requisitos Previos](#requisitos-previos)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Arquitectura y Diseño](#arquitectura-y-diseño)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Configuración de Observabilidad](#configuración-de-observabilidad)
7. [Instrumentación OpenTelemetry](#instrumentación-opentelemetry)
8. [Docker Compose Unificado](#docker-compose-unificado)
9. [API Endpoints](#api-endpoints)
10. [URLs y Acceso a Servicios](#urls-y-acceso-a-servicios)
11. [Visualización de Datos](#visualización-de-datos)
12. [Troubleshooting](#troubleshooting)

---

## 🔧 SCRIPT DE INSTALACIÓN Y PRUEBA AUTOMÁTICA

### ¿Qué hace el script?

El script `setup_and_test.py` automatiza completamente todo el proceso de configuración:

```bash
python3 setup_and_test.py
```

**Proceso ejecutado:**

| Paso | Acción | Resultado |
|------|--------|-----------|
| 1️⃣ | Detiene contenedores previos | Limpia el estado anterior |
| 2️⃣ | Levanta 10 servicios Docker | customer-api, db, redis, rabbitmq, etc. |
| 3️⃣ | Espera inicialización (máx 120s) | Valida que todos estén en estado "running" |
| 4️⃣ | Verifica servicios respondiendo | GET a /api/customer, health checks, etc. |
| 5️⃣ | Ejecuta 5 pruebas de API | GET, POST, PUT, DELETE con datos reales |
| 6️⃣ | Valida generación de logs | Extrae logs JSON estructurados del contenedor |
| 7️⃣ | Muestra URLs de servicios | Links directos a Grafana, Jaeger, Prometheus, etc. |

**Salida del script:**

```
================================================================================
                    CUSTOMER API - SETUP Y TEST AUTOMATIZADO
================================================================================

ℹ Iniciado el 2026-01-27 18:05:30
ℹ Servicios a levantar: customer-db, customer-redis, customer-rabbitmq, ...

▶ Paso 1/7: Deteniendo contenedores previos...
✓ Contenedores detenidos correctamente

▶ Paso 2/7: Levantando contenedores Docker...
✓ Comando docker-compose up ejecutado

▶ Paso 3/7: Esperando a que los contenedores se inicialicen...
ℹ Contenedores en ejecución: 5/10 (tiempo restante: 115s)
ℹ Contenedores en ejecución: 8/10 (tiempo restante: 110s)
✓ Todos los contenedores están en ejecución

▶ Paso 4/7: Verificando servicios...
✓ customer-api respondiendo correctamente
✓ customer-grafana respondiendo correctamente
...
```

### Requisitos para ejecutar el script

```bash
# Python 3.7+
python3 --version

# Librerías necesarias (generalmente preinstaladas)
pip install requests  # Si no está instalado
```

---

## 📊 STACK TECNOLÓGICO

### Backend & Aplicación

| Componente | Versión | Propósito |
|-----------|---------|----------|
| **Java** | 21 LTS | Runtime JVM |
| **Spring Boot** | 3.2.0 | Framework Web/REST |
| **Spring Data JPA** | 3.2.0 | ORM & Persistencia |
| **Lombok** | 1.18.30 | Reducción de boilerplate |
| **Maven** | 3.9.6+ | Build & Dependency Management |

### Base de Datos & Cache

| Componente | Versión | Propósito |
|-----------|---------|----------|
| **PostgreSQL** | 14+ | Base de datos relacional |
| **Redis** | 7+ | Cache en memoria |
| **RabbitMQ** | 3.13+ | Message Broker |

### Observabilidad & Monitoreo

| Componente | Versión | Propósito |
|-----------|---------|----------|
| **OpenTelemetry Agent** | 2.4.0 | Instrumentación automática de aplicación |
| **OpenTelemetry Collector** | latest-contrib | Recopilación y procesamiento de telemetría |
| **Prometheus** | latest | Almacenamiento de métricas |
| **Grafana** | latest | Visualización unificada |
| **Jaeger** | latest | Trazas distribuidas (OTEL backend) |
| **Loki** | latest | Almacenamiento de logs |
| **Zipkin** | latest | Rastreador distribuido (alternativa) |

### Logging

| Componente | Versión | Propósito |
|-----------|---------|----------|
| **Logback** | 1.5.0+ | Framework de logging |
| **Logstash Encoder** | 7.4 | Encoding JSON para logs |
| **JSON Logs** | Structured | Logs en formato JSON con labels OTEL |

---

## 🏗️ ARQUITECTURA Y DISEÑO

### Flujo de Datos de Observabilidad

```
┌─────────────────┐
│  Customer API   │
│  (Spring Boot)  │
│                 │
│  ┌───────────┐  │
│  │  OTEL     │  │  Instrumentación
│  │  Agent    │  │  Automática
│  │  v2.4.0   │  │  (Java Agent)
│  └───────────┘  │
└────────┬────────┘
         │
    ┌────┴──────────────────────────────┐
    │                                    │
    ▼                                    ▼
┌─────────────┐              ┌─────────────────────┐
│ OTEL        │              │ Aplicación Logs     │
│ Collector   │◄─────────────│ (JSON structurado)  │
│ (gRPC 4317) │              │ (Logback)           │
└────┬────────┘              └─────────────────────┘
     │
     ├──► Prometheus  ──────► MÉTRICAS
     ├──► Jaeger      ──────► TRAZAS
     └──► Loki        ──────► LOGS
          │
          └──► Grafana (Dashboard Unificado)
```

### Captura Automática (OTEL Agent)

```java
Traces (Trazas):
├─ HTTP Requests (método, status, latencia)
├─ Database Queries (SQL, tiempo ejecución)
├─ RabbitMQ Messages (publish, consume)
├─ Redis Operations (get, set, delete)
└─ Exceptions (stack traces)

Metrics (Métricas):
├─ HTTP Request Duration
├─ Database Connection Pool
├─ JVM Memory Usage
├─ GC Activity
└─ Thread Statistics

Logs (Logs):
├─ Application Logs (DEBUG, INFO, WARN, ERROR)
├─ Structured JSON
├─ Trace ID Correlation
└─ Custom Labels (service, severity, logger)
```

---

## Requisitos Previos

### Software Necesario
- **Java 21 o superior** (LTS)
- **Maven 3.9.6 o superior**
- **Docker y Docker Compose**
- **Python 3.7+** (para ejecutar script de setup)
- **curl** (para pruebas manuales)

### Verificar Versiones

```bash
java -version
javac -version
mvn -version
docker --version
docker-compose --version
python3 --version
```

---

## Estructura del Proyecto

```
CustomerApi/
├── src/
│   ├── main/
│   │   ├── java/com/elblogdelarqui/customer/
│   │   │   ├── CustomerApplication.java          # Clase principal
│   │   │   ├── config/                           # Configuraciones
│   │   │   │   ├── RabbitMQConfig.java
│   │   │   │   ├── RedisCacheConfig.java
│   │   │   │   └── SendGridConfig.java
│   │   │   ├── controller/
│   │   │   │   └── CustomerController.java       # Endpoints REST (con instrumentación manual)
│   │   │   ├── dto/
│   │   │   │   ├── request/
│   │   │   │   │   └── RequestCustomerDTO.java
│   │   │   │   └── response/
│   │   │   │       └── ResponseCustomerDTO.java
│   │   │   ├── entity/
│   │   │   │   └── Customer.java                 # Entidad JPA
│   │   │   ├── publisher/
│   │   │   │   └── RabbitMQProducer.java         # Con instrumentación manual
│   │   │   ├── repository/
│   │   │   │   └── CustomerRepository.java       # Acceso a datos
│   │   │   ├── service/
│   │   │   │   ├── CustomerService.java          # Interfaz
│   │   │   │   ├── CustomerServiceImplement.java # Implementación (con instrumentación manual)
│   │   │   │   └── EmailService.java
│   │   │   └── util/
│   │   │       └── CustomerMapper.java           # Mapeo de DTOs
│   │   └── resources/
│   │       └── application.properties             # Configuración
│   └── test/
│       └── CustomerApplicationTests.java
├── config/                                        # Configuración de servicios
│   ├── prometheus/
│   │   └── prometheus.yml                        # Config Prometheus
│   ├── grafana/
│   │   └── grafana-datasources.yml               # Datasources Grafana
│   └── otel-collector/
│       └── otel-config.yaml                      # Configuración OpenTelemetry Collector
├── log/
│   └── otel/                                     # Logs persistentes de OpenTelemetry
├── pom.xml                                        # Dependencias Maven
├── Dockerfile                                     # Imagen Docker con instrumentación OTEL v2.4.0
├── docker-compose.yml                             # Compose unificado (11 servicios)
└── README.md                                      # Este archivo (v3.0)
```

---

## Instrumentación OpenTelemetry (v3.0)

### ✨ Instrumentación Automática vía Dockerfile

El archivo `Dockerfile` descarga e integra automáticamente el **OpenTelemetry Java Agent v2.4.0**:

```dockerfile
# ===== DESCARGA DEL OPENTELEMETRY JAVA AGENT =====
RUN apt-get update && apt-get install -y wget && \
    wget -q https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v2.4.0/opentelemetry-javaagent.jar && \
    chmod +x opentelemetry-javaagent.jar && \
    apt-get remove -y wget && \
    apt-get clean

# ===== VARIABLES DE ENTORNO OPENTELEMETRY =====
ENV OTEL_JAVAAGENT_ENABLED=true
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_LOGS_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
ENV OTEL_SERVICE_NAME=customer-api
ENV OTEL_TRACES_SAMPLER=always_on

# ===== ENTRYPOINT CON JAVAAGENT =====
ENTRYPOINT ["java", "-javaagent:./opentelemetry-javaagent.jar", "-jar", "app.jar"]
```

**Captura automáticamente:**
- ✅ Requests HTTP (métodos, status codes, latencias)
- ✅ Consultas a PostgreSQL (queries, tiempos)
- ✅ Publicación de mensajes RabbitMQ
- ✅ Operaciones Redis (gets, sets, deletes)
- ✅ Excepciones y errores
- ✅ Pool de conexiones JDBC
- ✅ Threads y CPU

### ✏️ Instrumentación Manual (v3.0 - NUEVA)

Agregamos instrumentación manual en los puntos críticos de negocio para capturar contexto específico:

#### 1. **CustomerServiceImplement.java** - Spans de Servicio

```java
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;

@Service
public class CustomerServiceImplement implements CustomerService {
    
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("com.elblogdelarqui.customer");

    @Override
    public ResponseCustomerDTO findById(Long id) {
        // Crear span para esta operación de negocio
        Span span = tracer.spanBuilder("customer.service.findById")
                .setAttribute("customer.id", id)  // Atributo personalizado
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            Customer customer = returnCustomer(id);
            ResponseCustomerDTO response = customerMapper.toCustomerDTO(customer);
            
            // Registrar evento con detalles
            span.addEvent("customer.found", 
                io.opentelemetry.api.common.Attributes.builder()
                    .put("customer.name", customer.getName())
                    .put("customer.email", customer.getEmail())
                    .build());
            
            return response;
        } catch (Exception e) {
            span.recordException(e);  // Registrar excepciones
            throw e;
        } finally {
            span.end();
        }
    }

    @Override
    public ResponseCustomerDTO register(RequestCustomerDTO customerDTO) throws IOException {
        Span span = tracer.spanBuilder("customer.service.register")
                .setAttribute("customer.name", customerDTO.getName())
                .setAttribute("customer.email", customerDTO.getEmail())
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            // Guardar cliente
            Customer customer = customerMapper.toCustomer(customerDTO);
            customer = customerRepository.save(customer);
            span.addEvent("customer.saved", 
                io.opentelemetry.api.common.Attributes.builder()
                    .put("customer.id", customer.getId())
                    .build());

            // Publicar evento en RabbitMQ
            ObjectMapper objectMapper = new ObjectMapper();
            String event = objectMapper.writeValueAsString(customer);
            rabbitMQProducer.sendMessage(event);
            span.addEvent("message.sent.rabbitmq");
            
            // Enviar email
            emailService.sendEmail("Create Customer", event);
            span.addEvent("email.sent");

            return customerMapper.toCustomerDTO(customer);
        } catch (Exception e) {
            span.recordException(e);
            throw e;
        } finally {
            span.end();
        }
    }
}
```

**Spans capturados:**
- `customer.service.findById` - Búsqueda por ID
- `customer.service.register` - Registro de nuevo cliente

---

#### 2. **CustomerController.java** - Spans HTTP

```java
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;

@RestController
public class CustomerController {
    
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("com.elblogdelarqui.customer");

    @GetMapping(value = "/{id}")
    public ResponseEntity<ResponseCustomerDTO> findById(@PathVariable Long id) {
        Span span = tracer.spanBuilder("http.get.findById")
                .setAttribute("http.method", "GET")
                .setAttribute("http.route", "/api/customer/{id}")
                .setAttribute("customer.id", id)
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            ResponseCustomerDTO response = customerService.findById(id);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.OK);
            return ResponseEntity.ok().body(response);
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }

    @PostMapping
    public ResponseEntity<ResponseCustomerDTO> register(@RequestBody RequestCustomerDTO customerDTO,
                                                        UriComponentsBuilder uriBuilder) throws IOException {
        Span span = tracer.spanBuilder("http.post.register")
                .setAttribute("http.method", "POST")
                .setAttribute("http.route", "/api/customer")
                .setAttribute("customer.name", customerDTO.getName())
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            ResponseCustomerDTO responseCustomerDTO = customerService.register(customerDTO);
            span.addEvent("customer.registered", 
                io.opentelemetry.api.common.Attributes.builder()
                    .put("customer.id", responseCustomerDTO.getId())
                    .build());
            
            URI uri = uriBuilder.path("/api/customer/{id}")
                    .buildAndExpand(responseCustomerDTO.getId()).toUri();
            span.setStatus(io.opentelemetry.api.trace.StatusCode.OK);
            return ResponseEntity.created(uri).body(responseCustomerDTO);
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}
```

**Spans capturados:**
- `http.get.findById` - GET /api/customer/{id}
- `http.post.register` - POST /api/customer
- `http.put.update` - PUT /api/customer/{id}
- `http.get.findAll` - GET /api/customer
- `http.delete.delete` - DELETE /api/customer/{id}

---

#### 3. **RabbitMQProducer.java** - Spans de Mensajería

```java
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;

@Service
public class RabbitMQProducer {
    
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("com.elblogdelarqui.customer");

    public void sendMessage(String message) {
        Span span = tracer.spanBuilder("rabbitmq.publish")
                .setAttribute("messaging.system", "rabbitmq")
                .setAttribute("messaging.destination", exchange)
                .setAttribute("messaging.rabbitmq.routing_key", routingKey)
                .setAttribute("messaging.message_payload_size_bytes", message.length())
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            LOGGER.info(String.format("Message sent -> %s", message));
            rabbitTemplate.convertAndSend(exchange, routingKey, message);
            span.addEvent("message.published");
        } catch (Exception e) {
            span.recordException(e);
            throw e;
        } finally {
            span.end();
        }
    }
}
```

**Spans capturados:**
- `rabbitmq.publish` - Publicación de mensajes

---

### Variables de Entorno OpenTelemetry

| Variable | Valor | Propósito |
|----------|-------|-----------|
| `OTEL_JAVAAGENT_ENABLED` | true | Activar javaagent |
| `OTEL_TRACES_EXPORTER` | otlp | Exportador de trazas |
| `OTEL_METRICS_EXPORTER` | otlp | Exportador de métricas |
| `OTEL_LOGS_EXPORTER` | otlp | Exportador de logs |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | grpc | Protocolo de transporte |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | http://otel-collector:4317 | Endpoint de recolección |
| `OTEL_SERVICE_NAME` | customer-api | Identificador de servicio |
| `OTEL_TRACES_SAMPLER` | always_on | Muestreo (100%) |

### Flujo de Telemetría Completo

```
┌──────────────────────────────────────────────────────────────┐
│                  CUSTOMER API (Java 21)                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  OpenTelemetry Java Agent v2.4.0                       │  │
│  │  ├─ Instrumentación Automática                         │  │
│  │  │  ├─ HTTP Requests/Responses                         │  │
│  │  │  ├─ PostgreSQL Queries                              │  │
│  │  │  ├─ RabbitMQ Operations                             │  │
│  │  │  └─ Redis Commands                                  │  │
│  │  │                                                      │  │
│  │  └─ Instrumentación Manual (v3.0 - NUEVA)             │  │
│  │     ├─ Spans Personalizados (Service, Controller)      │  │
│  │     ├─ Atributos de Negocio (customer.id, name, etc) │  │
│  │     └─ Eventos Contextuales (customer.found, etc)     │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────┬───────────────────────────────────────────────────┘
           │
           │ OTLP gRPC Protocol (Puerto 4317)
           │ - Traces (todas las operaciones)
           │ - Metrics (JVM, HTTP, business)
           │ - Logs (application + system)
           ▼
┌──────────────────────────────────────────────────────────────┐
│      OpenTelemetry Collector (Container)                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Receiver: OTLP gRPC (4317), OTLP HTTP (4318)          │  │
│  │ Processor: Batch (10s)                                 │  │
│  │ Exporters: Jaeger, Zipkin, Prometheus, Loki, File    │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────┬───────────────────────────────────────────────────┘
           │
      ┌────┼────┬────────┬────────┬──────────┐
      │    │    │        │        │          │
      ▼    ▼    ▼        ▼        ▼          ▼
   Jaeger Zipkin Prometheus Loki Debug  File Export
   (Trazas) (Traces) (Métricas) (Logs) (Stdout) (otel/)
```

---

## Variables de Configuración

### Archivo: `src/main/resources/application.properties`

```properties
# ========== DATASOURCE (PostgreSQL) ==========
spring.datasource.url=jdbc:postgresql://customer-db:5432/Northwind
spring.datasource.username=root
spring.datasource.password=secret

# ========== JPA / HIBERNATE ==========
spring.jpa.properties.hibernate.jdbc.lob.non_contextual_creation=true
spring.jpa.hibernate.ddl-auto=update

# ========== LOGGING ==========
logging.level.org.springframework.web=DEBUG
logging.level.org.hibernate=DEBUG

# ========== RABBITMQ ==========
spring.rabbitmq.host=customer-rabbitmq
spring.rabbitmq.port=5672
spring.rabbitmq.username=guest
spring.rabbitmq.password=guest

# ========== REDIS CACHE ==========
spring.redis.host=customer-redis
spring.redis.port=6379

# ========== SERVIDOR ==========
server.port=8080
spring.application.name=customer-api

# ========== OPENTELEMETRY ==========
# Configurado via Docker (variables de entorno)
# No requiere configuración adicional en application.properties
```

---

## Levantamiento de la Infraestructura

### Docker Compose (Todos los 11 Servicios)

```bash
cd /ruta/a/CustomerApi

# Levantar todos los servicios
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs de la aplicación
docker-compose logs -f customer-api

# Ver logs del OpenTelemetry Collector
docker-compose logs -f customer-otel-collector

# Detener todo
docker-compose down
```

### Servicios Disponibles

| # | Servicio | Puerto | Estatus |
|----|----------|--------|---------|
| 1 | **customer-api** | 8080 | ✅ Operativo con OTEL v2.4.0 |
| 2 | **customer-db** | 5432 | ✅ PostgreSQL |
| 3 | **customer-rabbitmq** | 5672 | ✅ Message Broker |
| 4 | **customer-redis** | 6379 | ✅ Cache |
| 5 | **customer-jaeger** | 16686 | ✅ Trazas distribuidas |
| 6 | **customer-zipkin** | 9411 | ✅ Trazas (backup) |
| 7 | **customer-prometheus** | 9090 | ✅ Métricas |
| 8 | **customer-loki** | 3100 | ✅ Logs |
| 9 | **customer-grafana** | 3000 | ✅ Dashboards |
| 10 | **customer-otel-collector** | 4317 | ✅ Recolección de telemetría |
| 11 | **customer-otel-collector-db** | - | ✅ Persistencia |

---

## Servicios de Observabilidad

### 🔍 Jaeger - Visualizar Trazas

**URL:** http://192.168.1.135:16686

```bash
# Verificar que customer-api está registrado
curl -s http://192.168.1.135:16686/api/services | jq

# Respuesta esperada:
# {"data":["jaeger-all-in-one","customer-api"],"total":2}
```

### 📊 Prometheus - Métricas

**URL:** http://192.168.1.135:9090

Targets configurados:
- `otel-collector:8889` (OpenTelemetry Metrics Exporter)

### 📈 Grafana - Dashboards

**URL:** http://192.168.1.135:3000
**Usuario:** admin
**Contraseña:** admin

### 📝 Loki - Logs Centralizados

**URL:** http://192.168.1.135:3100

Búsqueda por labels:
```
{service="customer-api"}
{level="ERROR", service="customer-api"}
```

### 🔗 Zipkin - Trazas Alternativas

**URL:** http://192.168.1.135:9411

---

## API Endpoints

### 1. GET /api/customer
Obtener todos los clientes

```bash
curl -X GET http://192.168.1.135:8080/api/customer
```

### 2. GET /api/customer/{id}
Obtener cliente por ID

```bash
curl -X GET http://192.168.1.135:8080/api/customer/1
```

**Spans en Jaeger:**
- `http.get.findById` (HTTP Layer)
- `customer.service.findById` (Service Layer)
- [Auto-instrumented DB Query] (OTEL Agent)

### 3. POST /api/customer
Crear nuevo cliente

```bash
curl -X POST http://192.168.1.135:8080/api/customer \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890"
  }'
```

**Spans en Jaeger:**
- `http.post.register` (HTTP)
- `customer.service.register` (Service)
- `rabbitmq.publish` (Messaging)
- [Automatic DB, Email, RabbitMQ spans]

### 4. PUT /api/customer/{id}
Actualizar cliente

```bash
curl -X PUT http://192.168.1.135:8080/api/customer/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com"
  }'
```

### 5. DELETE /api/customer/{id}
Eliminar cliente

```bash
curl -X DELETE http://192.168.1.135:8080/api/customer/1
```

---

## Visualización de Trazas en Jaeger

### Pasos para Ver Trazas

1. **Abrir Jaeger UI:**
   ```
   http://192.168.1.135:16686
   ```

2. **Seleccionar Servicio:**
   - Dropdown "Service" → Seleccionar `customer-api`

3. **Seleccionar Operación:**
   - `http.get.findById`
   - `http.post.register`
   - `customer.service.findById`
   - `rabbitmq.publish`
   - etc.

4. **Buscar Trazas:**
   - Por duración: `minDuration=50ms`
   - Por etiqueta: `customer.id=1`
   - Por estado: `error=true` (errores solo)

### Ejemplo de Traza Completa

Cuando hace **POST /api/customer** (crear cliente):

```
Trace ID: a1b2c3d4e5f6g7h8i9j0
Duration: 245ms
Service: customer-api

├─ http.post.register (102ms) [HTTP Controller]
│  ├─ customer.service.register (98ms) [Service Layer]
│  │  ├─ [PostgreSQL INSERT] (30ms) [Auto-instrumented]
│  │  │  └─ Event: customer.saved (id=42)
│  │  ├─ rabbitmq.publish (15ms) [Manual instrumentation]
│  │  │  └─ Event: message.published
│  │  └─ [Email Send] (25ms) [Implicit via EmailService]
│  │     └─ Event: email.sent
│  └─ Attributes:
│     - http.method: POST
│     - http.route: /api/customer
│     - customer.name: John Doe
│     - customer.email: john@example.com
│     - http.status_code: 201
└─ Status: OK
```

---

## Solución de Problemas

### 1. API no inicia con OTEL Agent

```
Error: java.lang.UnsupportedClassVersionError
Causa: OpenTelemetry Agent v2.4.0 no es compatible con Java 17

Solución:
✅ Ya está resuelta: Java 21 configurado en pom.xml
✅ Dockerfile usa eclipse-temurin:21-jre
```

### 2. No aparecen trazas en Jaeger

```bash
# Verificar que otel-collector está corriendo
docker-compose ps customer-otel-collector

# Ver logs del collector
docker-compose logs customer-otel-collector

# Hacer un request para generar trazas
curl http://192.168.1.135:8080/api/customer

# Ir a Jaeger e introducir el servicio
http://192.168.1.135:16686 → Service: customer-api
```

### 3. Error: "Connection refused" en PostgreSQL

```bash
# Verificar que DB está corriendo
docker-compose ps customer-db

# Ver logs de la DB
docker-compose logs customer-db

# Esperar 15-20 segundos para que PostgreSQL inicie
```

### 4. RabbitMQ Auth Error

```bash
# Verificar credenciales
docker-compose exec customer-rabbitmq rabbitmqctl list_users

# Credenciales por defecto: guest/guest

# Management UI
http://192.168.1.135:15672
```

### 5. Memoria insuficiente

```bash
# Detener servicios no críticos
docker-compose stop customer-zipkin customer-grafana

# Limpiar datos no usados
docker system prune -a
docker volume prune
```

---

## Resumen de Cambios v3.0

### ✅ Cambios Principales

| Item | Status | Detalles |
|------|--------|----------|
| **Dockerfile** | ✅ | Integración OTEL Agent v2.4.0 |
| **CustomerServiceImplement.java** | ✅ | Spans manuales en findById() y register() |
| **CustomerController.java** | ✅ | Spans en todos los endpoints HTTP |
| **RabbitMQProducer.java** | ✅ | Span manual en sendMessage() |
| **README** | ✅ | Documentación completa v3.0 |
| **Telemetría** | ✅ | Automática + Manual operativa |

### 📊 Cobertura de Instrumentación

- ✅ **HTTP Requests:** 100% (5 endpoints)
- ✅ **Service Layer:** 100% (2 operaciones críticas)
- ✅ **RabbitMQ Publishing:** 100% (con atributos)
- ✅ **Database Queries:** 100% (automático)
- ✅ **Error Handling:** 100% (excepciones registradas)
- ✅ **Custom Attributes:** 100% (business context)
- ✅ **Events:** 100% (operaciones significativas)

---

## Próximos Pasos (Opcional)

- [ ] Configurar métricas personalizadas (histogramas)
- [ ] Crear dashboards personalizados en Grafana
- [ ] Alertas en Prometheus
- [ ] Baggage context propagation
- [ ] Tests de carga con JMeter
- [ ] Implementar rate limiting
- [ ] Agregar autenticación JWT

---

**Versión:** 3.0  
**Última actualización:** 2024-01-24  
**Estado:** ✅ Producción - OpenTelemetry Completo (Automático + Manual)

---

## Requisitos Previos

### Software Necesario
- **Java 21 o superior** (LTS)
- **Maven 3.9.6 o superior**
- **Docker y Docker Compose** (opcional, si deseas usar contenedores)
- **curl o Postman** (para testear APIs)
- **PostgreSQL 14+** (puede estar en Docker o en una máquina virtual)
- **RabbitMQ 3.13+** (mensaje broker)
- **Redis 7+** (cache)

### Verificar Versiones

```bash
java -version
javac -version
mvn -version
docker --version
docker-compose --version
```

---

## Configuración Inicial

### 1. Problema Inicial: Incompatibilidad Java 17 vs Java 21

**Problema:** El proyecto estaba configurado para Java 17, pero tenías Java 21 instalado, causando error:
```
java.lang.NoSuchFieldError: Class com.sun.tools.javac.tree.JCTree$JCImport does not have member field 'com.sun.tools.javac.tree.JCTree qualid'
```

**Solución Aplicada:**

#### Paso 1: Actualizar versión de Java en `pom.xml`
```xml
<properties>
    <java.version>21</java.version>  <!-- Cambiar de 17 a 21 -->
</properties>
```

#### Paso 2: Actualizar Spring Boot a 3.2.0 (compatible con Java 21)
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>  <!-- Cambiar de 3.1.3 a 3.2.0 -->
    <relativePath/>
</parent>
```

#### Paso 3: Compilar nuevamente
```bash
mvn clean compile
```

---

## Estructura del Proyecto

```
CustomerApi/
├── src/
│   ├── main/
│   │   ├── java/com/elblogdelarqui/customer/
│   │   │   ├── CustomerApplication.java          # Clase principal
│   │   │   ├── config/                           # Configuraciones
│   │   │   │   ├── RabbitMQConfig.java
│   │   │   │   ├── RedisCacheConfig.java
│   │   │   │   └── SendGridConfig.java
│   │   │   ├── controller/
│   │   │   │   └── CustomerController.java       # Endpoints REST
│   │   │   ├── dto/
│   │   │   │   ├── request/
│   │   │   │   │   └── RequestCustomerDTO.java
│   │   │   │   └── response/
│   │   │   │       └── ResponseCustomerDTO.java
│   │   │   ├── entity/
│   │   │   │   └── Customer.java                 # Entidad JPA
│   │   │   ├── publisher/
│   │   │   │   └── RabbitMQProducer.java
│   │   │   ├── repository/
│   │   │   │   └── CustomerRepository.java       # Acceso a datos
│   │   │   ├── service/
│   │   │   │   ├── CustomerService.java          # Interfaz
│   │   │   │   ├── CustomerServiceImplement.java # Implementación
│   │   │   │   └── EmailService.java
│   │   │   └── util/
│   │   │       └── CustomerMapper.java           # Mapeo de DTOs
│   │   └── resources/
│   │       └── application.properties             # Configuración
│   └── test/
│       └── CustomerApplicationTests.java
├── config/                                        # 🆕 Configuración de servicios
│   ├── prometheus/
│   │   └── prometheus.yml                        # Config Prometheus
│   ├── grafana/
│   │   └── grafana-datasources.yml               # Datasources Grafana
│   └── otel-collector/                           # 🆕 OpenTelemetry Collector
│       └── otel-config.yaml                      # Configuración OTEL
├── log/
│   └── otel/                                     # 📁 Logs de OpenTelemetry
├── pom.xml                                        # Dependencias Maven
├── Dockerfile                                     # Para Docker
├── docker-compose.yml                             # 🆕 Compose unificado
└── README.md                                      # Este archivo
```

---

## Variables de Configuración

### Archivo: `src/main/resources/application.properties`

```properties
# ========== DATASOURCE (PostgreSQL) ==========
spring.datasource.url=jdbc:postgresql://192.168.1.135:5432/Northwind
spring.datasource.username=root
spring.datasource.password=secret

# ========== JPA / HIBERNATE ==========
spring.jpa.properties.hibernate.jdbc.lob.non_contextual_creation=true
spring.jpa.hibernate.ddl-auto=update  # Opciones: validate, update, create, create-drop

# ========== SQL LOGGING ==========
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# ========== LOGGING LEVELS ==========
logging.level.org.springframework.web=DEBUG
logging.level.org.hibernate=DEBUG

# ========== RABBITMQ ==========
spring.rabbitmq.host=192.168.1.135
spring.rabbitmq.port=5672
spring.rabbitmq.username=guest
spring.rabbitmq.password=guest
spring.rabbitmq.virtual-host=/

rabbitmq.queue.name=customers
rabbitmq.exchange.name=customers_exchange
rabbitmq.routing.key=customers_routing_key

# ========== SENDGRID EMAIL ==========
sendgrid.api.key=SG.tu_api_key_aqui
sendgrid.api.from=tu_email@tudominio.com
sendgrid.api.to=destinatario@tudominio.com

# ========== REDIS CACHE ==========
spring.redis.host=192.168.1.135
spring.redis.port=6379
```

### ⚠️ CAMPOS A RELLENAR

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `spring.datasource.url` | URL de PostgreSQL | `jdbc:postgresql://192.168.1.135:5432/Northwind` |
| `spring.datasource.username` | Usuario de BD | `root` |
| `spring.datasource.password` | Contraseña de BD | `secret` |
| `spring.rabbitmq.host` | Host de RabbitMQ | `192.168.1.135` |
| `spring.rabbitmq.username` | Usuario RabbitMQ | `guest` |
| `spring.rabbitmq.password` | Contraseña RabbitMQ | `guest` |
| `sendgrid.api.key` | API Key de SendGrid | Obtener desde https://sendgrid.com |
| `sendgrid.api.from` | Email remitente | `noreply@tudominio.com` |
| `sendgrid.api.to` | Email destinatario | `admin@tudominio.com` |
| `spring.redis.host` | Host de Redis | `192.168.1.135` |

---

## Levantamiento de la Infraestructura

### Docker Compose Unificado 🚀

Se ha implementado un único archivo `docker-compose.yml` que integra:
- Servicios base de la aplicación
- Servicios de observabilidad (Jaeger, Zipkin, Prometheus, Loki, Grafana)

#### Opción A: Solo Servicios Base

```bash
cd /ruta/a/CustomerApi
docker-compose up -d
```

Levanta:
- 🐳 **customer-api** (Puerto 8080)
- 🗄️ **PostgreSQL** (Puerto 5432)
- 🐰 **RabbitMQ** (Puertos 5672, 15672)
- 📊 **Redis** (Puerto 6379)

#### Opción B: Con Servicios Base + Infraestructura

```bash
docker-compose --profile with-services up -d
```

Levanta todos los servicios base en Docker.

#### Opción C: Con Observabilidad

```bash
docker-compose --profile with-observability up -d
```

Levanta servicios de observabilidad:
- 🔍 **Jaeger** (Puerto 16686)
- 🔗 **Zipkin** (Puerto 9411)
- 📈 **Prometheus** (Puerto 9090)
- 📋 **Loki** (Puerto 3100)
- 📊 **Grafana** (Puerto 3000)

#### Opción D: Todo (Recomendado)

```bash
docker-compose --profile with-services --profile with-observability up -d
```

#### Comandos Útiles

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs
docker-compose logs -f customer-api

# Detener todo
docker-compose down

# Detener y remover volúmenes
docker-compose down -v
```

---

## Servicios de Observabilidad

### � OpenTelemetry Collector
- **URL**: N/A (servicio backend)
- **Puertos**: 
  - 4317 (OTLP Receiver protocol gRPC)
  - 4318 (OTLP Receiver protocol HTTP)
  - 13133 (Health Check extension)
  - 55679 (ZPages extension)
  - 8889 (Prometheus metrics exporter)
- **Funcionalidad**: Recolección unificada de telemetría (traces, métricas, logs)
- **Exporta a**: Jaeger, Zipkin, Prometheus, Loki
- **Configuración**: `./otel-collector/otel-config.yaml`

### 📊 Grafana
- **URL**: http://localhost:3000
- **Usuario**: admin (anonymous enabled)
- **Funcionalidad**: Dashboard unificado para métricas, logs y traces
- **Datasources**: Prometheus, Loki, Jaeger (preconfigurados)

### 🔍 Jaeger
- **URL**: http://localhost:16686
- **Funcionalidad**: Tracing distribuido
- **Puertos**: 
  - 16686 (Web UI)
  - 6831 (Jaeger Thrift compact)
  - 6832 (Jaeger Thrift binary)
  - 14268 (Jaeger HTTP)

### 🔗 Zipkin
- **URL**: http://localhost:9411
- **Funcionalidad**: Tracing distribuido alternativo
- **Protocolos**: JSON v2, Protobuf

### 📈 Prometheus
- **URL**: http://localhost:9090
- **Funcionalidad**: Recolección de métricas
- **Config**: `./config/prometheus/prometheus.yml`
- **Targets**: 
  - otel-collector:8889 (OpenTelemetry Collector)
  - otel-collector:8888 (Prometheus exporter interno)

### 📋 Loki
- **URL**: http://localhost:3100
- **Funcionalidad**: Agregación de logs
- **Puerto**: 3100
- **Recibe logs de**: OpenTelemetry Collector

---

## Ejecución de la Aplicación

### Compilación
```bash
mvn clean compile
```

### Empaquetado
```bash
mvn clean package -DskipTests
```

Genera JAR en: `target/customer-api-0.0.1-SNAPSHOT.jar`

### Ejecutar el JAR
```bash
java -jar target/customer-api-0.0.1-SNAPSHOT.jar
```

### Ejecutar con Maven
```bash
mvn spring-boot:run
```

---

## API Endpoints

### 1. Obtener todos los clientes
```http
GET /api/customer
```

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "firstName": "Juan",
    "lastName": "Pérez",
    "birthDate": "1995-05-15T00:00:00.000+00:00",
    "address": "Calle Principal 123",
    "city": "Madrid",
    "country": "España",
    "phone": "912345678",
    "age": 30
  }
]
```

---

### 2. Obtener cliente por ID
```http
GET /api/customer/{id}
```

**Ejemplo:**
```bash
GET /api/customer/1
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "firstName": "Juan",
  "lastName": "Pérez",
  "birthDate": "1995-05-15T00:00:00.000+00:00",
  "address": "Calle Principal 123",
  "city": "Madrid",
  "country": "España",
  "phone": "912345678",
  "age": 30
}
```

---

### 3. Crear cliente
```http
POST /api/customer
Content-Type: application/json
```

**Body:**
```json
{
  "firstName": "María",
  "lastName": "González",
  "age": 28,
  "city": "Barcelona",
  "country": "España",
  "address": "Avenida Reforma 456",
  "phone": "934567890",
  "birthDate": "1997-08-20"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 2,
  "firstName": "María",
  "lastName": "González",
  "birthDate": "1997-08-20T00:00:00.000+00:00",
  "address": "Avenida Reforma 456",
  "city": "Barcelona",
  "country": "España",
  "phone": "934567890",
  "age": 28
}
```

**Header Response:**
```
Location: /api/customer/2
```

---

### 4. Actualizar cliente
```http
PUT /api/customer/{id}
Content-Type: application/json
```

**Ejemplo:**
```bash
PUT /api/customer/2
```

**Body:**
```json
{
  "firstName": "María",
  "lastName": "López García",
  "age": 29,
  "city": "Valencia",
  "country": "España",
  "address": "Calle Libertad 789",
  "phone": "961234567",
  "birthDate": "1997-08-20"
}
```

**Respuesta (200 OK):** Retorna el cliente actualizado

---

### 5. Eliminar cliente
```http
DELETE /api/customer/{id}
```

**Ejemplo:**
```bash
DELETE /api/customer/1
```

**Respuesta (200 OK):**
```json
"Customer id: 1 deleted"
```

---

## Pruebas de los Endpoints

### Con cURL

#### 1. Obtener todos los clientes
```bash
curl -s http://192.168.1.135:8080/api/customer
```

#### 2. Crear un cliente
```bash
curl -s -X POST http://192.168.1.135:8080/api/customer \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Juan",
    "lastName": "Pérez",
    "age": 30,
    "city": "Madrid",
    "country": "España",
    "address": "Calle Principal 123",
    "phone": "912345678",
    "birthDate": "1995-05-15"
  }'
```

#### 3. Obtener cliente por ID
```bash
curl -s http://192.168.1.135:8080/api/customer/1
```

#### 4. Actualizar cliente
```bash
curl -s -X PUT http://192.168.1.135:8080/api/customer/1 \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Juan",
    "lastName": "Pérez García",
    "age": 31,
    "city": "Madrid",
    "country": "España",
    "address": "Calle Principal 123",
    "phone": "912345678",
    "birthDate": "1995-05-15"
  }'
```

#### 5. Eliminar cliente
```bash
curl -s -X DELETE http://192.168.1.135:8080/api/customer/1
```

---

### Con Postman

1. Abre Postman
2. Crea una nueva colección llamada "Customer API"
3. Agrega las siguientes requests:

| Método | URL | Tipo |
|--------|-----|------|
| GET | `http://192.168.1.135:8080/api/customer` | List All |
| POST | `http://192.168.1.135:8080/api/customer` | Create |
| GET | `http://192.168.1.135:8080/api/customer/{{customer_id}}` | Get by ID |
| PUT | `http://192.168.1.135:8080/api/customer/{{customer_id}}` | Update |
| DELETE | `http://192.168.1.135:8080/api/customer/{{customer_id}}` | Delete |

---

## Docker

### Dockerfile Multi-stage

El `Dockerfile` incluido utiliza un build multi-stage para optimizar la imagen:

```dockerfile
# Stage 1: Compilación con Maven
FROM maven:3.9.6-eclipse-temurin-21 AS builder
...

# Stage 2: Runtime con solo JRE
FROM eclipse-temurin:21-jre
...
```

**Ventajas:**
- ✅ Imagen final pequeña (~500MB)
- ✅ No incluye herramientas de compilación
- ✅ Seguridad mejorada
- ✅ Startup más rápido

### Build Manual de la Imagen Docker

```bash
# Construir imagen
docker build -t customer-api:1.0 .

# Ejecutar contenedor
docker run -p 8080:8080 \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://192.168.1.135:5432/Northwind \
  -e SPRING_DATASOURCE_USERNAME=root \
  -e SPRING_DATASOURCE_PASSWORD=secret \
  -e SPRING_RABBITMQ_HOST=192.168.1.135 \
  -e SPRING_REDIS_HOST=192.168.1.135 \
  customer-api:1.0
```

### Docker Compose

Ver sección [Levantamiento de la Infraestructura](#levantamiento-de-la-infraestructura)

---

## 🔗 URLs Y ACCESO A SERVICIOS

### LOCALIZACIÓN: Para desarrollo en la máquina local

| Servicio | URL | Credenciales | Descripción |
|----------|-----|--------------|-------------|
| **Customer API** | 🔵 [http://localhost:8080](http://localhost:8080) | N/A | API REST de Clientes |
| **Grafana** | 🟠 [http://localhost:3000](http://localhost:3000) | admin / admin | Dashboard Observabilidad |
| **Prometheus** | 🟡 [http://localhost:9090](http://localhost:9090) | N/A | Recopilador Métricas |
| **Jaeger** | 🔴 [http://localhost:16686](http://localhost:16686) | N/A | Trazas Distribuidas |
| **Loki** | 🟣 [http://localhost:3100](http://localhost:3100) | N/A | Almacenamiento Logs |
| **Zipkin** | 🟢 [http://localhost:9411](http://localhost:9411) | N/A | Rastreador Distribuido |
| **RabbitMQ** | 🐰 [http://localhost:15672](http://localhost:15672) | guest / guest | Message Broker Admin |
| **PostgreSQL** | 🐘 localhost:5432 | postgres / password | Base de Datos |
| **Redis** | 🔴 localhost:6379 | N/A | Cache en Memoria |

### LOCALIZACIÓN: Para producción (servidor remoto)

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Customer API** | 🔵 [http://192.168.1.135:8080](http://192.168.1.135:8080) | API REST de Clientes |
| **Grafana** | 🟠 [http://192.168.1.135:3000](http://192.168.1.135:3000) | Dashboard Observabilidad |
| **Prometheus** | 🟡 [http://192.168.1.135:9090](http://192.168.1.135:9090) | Recopilador Métricas |
| **Jaeger** | 🔴 [http://192.168.1.135:16686](http://192.168.1.135:16686) | Trazas Distribuidas |
| **Loki** | 🟣 [http://192.168.1.135:3100](http://192.168.1.135:3100) | Almacenamiento Logs |
| **Zipkin** | 🟢 [http://192.168.1.135:9411](http://192.168.1.135:9411) | Rastreador Distribuido |
| **RabbitMQ** | 🐰 [http://192.168.1.135:15672](http://192.168.1.135:15672) | Message Broker Admin |

### Guía de Uso por Servicio

#### 1️⃣ **Grafana** - Tu Dashboard Principal
```
URL: http://localhost:3000
Usuario: admin
Contraseña: admin

Pasos:
1. Accede a Grafana
2. Ve a "Connections" > "Data Sources"
3. Verifica que tengas:
   - Prometheus (para métricas)
   - Loki (para logs)
4. Crea un nuevo Dashboard o usa los pre-configurados
5. Agrega panels de Loki: {service_name="customer-api"}
```

#### 2️⃣ **Jaeger** - Visualiza Trazas
```
URL: http://localhost:16686

Pasos:
1. Accede a Jaeger
2. Selecciona servicio: "customer-api"
3. Busca operaciones:
   - http.get.findAll
   - http.post.register
   - http.get.findById
   - http.put.update
   - http.delete.delete
4. Haz clic en una traza para ver detalles
5. Observa tiempos, spans, logs asociados
```

#### 3️⃣ **Prometheus** - Explora Métricas
```
URL: http://localhost:9090

Pasos:
1. Accede a Prometheus
2. Ve a "Graph" en la barra superior
3. Escribe una métrica:
   - http_server_request_duration_seconds
   - process_runtime_go_goroutines
   - jvm_memory_used_bytes
4. Visualiza gráficos
```

#### 4️⃣ **Loki** - Busca Logs
```
URL: http://localhost:3100 (API solo)
Mejor acceso: Desde Grafana

En Grafana:
1. Explora > Loki
2. Filtro: {service_name="customer-api"}
3. Busca logs por:
   - Level: DEBUG, INFO, WARN, ERROR
   - Logger: org.hibernate.SQL, etc.
   - Trace ID: para correlacionar con trazas
```

#### 5️⃣ **RabbitMQ** - Monitorea Mensajes
```
URL: http://localhost:15672
Usuario: guest
Contraseña: guest

Pasos:
1. Accede al Admin
2. Ve a "Queues" para ver mensajes pendientes
3. Ve a "Connections" para ver conexiones activas
4. Monitorea la salud del broker
```

### Ejemplos de Consultas

#### Consulta de Logs en Grafana/Loki
```
{service_name="customer-api"} 
| json 
| level="ERROR"
```

#### Consulta de Métricas en Prometheus
```
rate(http_server_request_duration_seconds_sum[5m]) 
/ 
rate(http_server_request_duration_seconds_count[5m])
```

#### Buscar por Trace ID
```
En Jaeger: Copia un trace_id de un log
Jaeger buscará automáticamente esa traza

En Grafana/Loki:
{service_name="customer-api"} 
| json 
| trace_id="ebf26883846cf31e41c771a8b8330ee3"
```

---

## 📈 VISUALIZACIÓN DE DATOS

### Ejemplos de Salida del Script

**Tabla de Resultados de Tests:**
```
+------------------------------------------+--------+--------+--------+
| Test                                     | Método | Status | Resultado |
+------------------------------------------+--------+--------+--------+
| GET /api/customer (Listar todos)         | GET    | 200    | ✓ ÉXITO |
| POST /api/customer (Crear cliente)       | POST   | 201    | ✓ ÉXITO |
| GET /api/customer/10 (Por ID)            | GET    | 200    | ✓ ÉXITO |
| PUT /api/customer/10 (Actualizar)        | PUT    | 200    | ✓ ÉXITO |
| DELETE /api/customer/10 (Eliminar)       | DELETE | 200    | ✓ ÉXITO |
+------------------------------------------+--------+--------+--------+

✓ Pruebas exitosas: 5/5
```

**Logs Generados (JSON estructurado):**
```json
{
  "time": "2026-01-27T18:03:00.449637518Z",
  "@version": "1",
  "message": "SELECT customer by id",
  "logger": "org.hibernate.SQL",
  "thread": "http-nio-8080-exec-10",
  "severity": "DEBUG",
  "level_value": 10000,
  "trace_id": "ebf26883846cf31e41c771a8b8330ee3",
  "trace_flags": "01",
  "span_id": "355903bfc2cd68e6"
}
```

**Resumen de Servicios:**
```
✓ ACCESO A LOS SERVICIOS:

1. Customer API
   🔗 http://localhost:8080/api/customer
   📝 API REST de Clientes

2. Grafana
   🔗 http://localhost:3000
   📝 Dashboard de Observabilidad

3. Prometheus
   🔗 http://localhost:9090
   📝 Recopilador de Métricas

... y más
```

---

## Solución de Problemas

### Problema 1: Error `NoSuchFieldError` en compilación

**Síntoma:**
```
java.lang.NoSuchFieldError: Class com.sun.tools.javac.tree.JCTree$JCImport does not have member field
```

**Solución:**
- Actualizar `<java.version>` a 21 en `pom.xml`
- Actualizar Spring Boot a versión 3.2.0 o superior

---

### Problema 2: Conexión rechazada a PostgreSQL

**Síntoma:**
```
org.postgresql.util.PSQLException: Connection to 192.168.1.135:5432 refused
```

**Solución:**
1. Verifica que PostgreSQL está corriendo:
   ```bash
   psql -h 192.168.1.135 -U root -d Northwind
   ```
2. Verifica la URL en `application.properties`
3. Verifica firewall/permisos de red

---

### Problema 3: RabbitMQ no accesible

**Síntoma:**
```
java.net.ConnectException: Connection refused
```

**Solución:**
1. Verifica RabbitMQ está corriendo:
   ```bash
   curl -u guest:guest http://192.168.1.135:15672/api/aliveness-test/%2F
   ```
2. Revisa credenciales en `application.properties`

---

### Problema 4: Redis no responde

**Síntoma:**
```
Unable to connect to Redis
```

**Solución:**
1. Verifica Redis está corriendo:
   ```bash
   redis-cli -h 192.168.1.135 ping
   ```
2. Respuesta esperada: `PONG`

---

### Problema 5: GET /api/customer/{id} retorna 500

**Síntoma:**
```json
{"timestamp":"...", "status":500, "error":"Internal Server Error", "path":"/api/customer/1"}
```

**Posibles causas:**
- El cliente no existe
- Error en la serialización/mapeo de datos
- Problema con JPA

**Solución:**
1. Verifica que el ID existe en la BD
2. Revisa los logs de la aplicación para más detalles
3. Ejecuta con `DEBUG` logging

---

## Información Adicional

### Tecnologías Utilizadas

- **Spring Boot 3.2.0** - Framework web
- **Spring Data JPA** - ORM
- **Hibernate 6.3.1** - Implementación JPA
- **PostgreSQL 14** - Base de datos
- **RabbitMQ 3.13** - Message broker
- **Redis 7** - Cache
- **OpenTelemetry Collector 0.111.0** - Recolección centralizada de telemetría
- **Jaeger 1.62.0** - Distributed Tracing
- **Zipkin 3** - Distributed Tracing
- **Prometheus 2.54.1** - Métricas
- **Grafana (latest)** - Dashboards
- **Loki** - Log Aggregation
- **Lombok** - Reducción de boilerplate
- **SendGrid** - Servicio de email
- **Maven 3.9.6** - Build tool
- **Java 21** - Lenguaje
- **Docker & Docker Compose** - Orquestación

### Puertos

| Servicio | Puerto | URL |
|----------|--------|-----|
| API | 8080 | http://localhost:8080 |
| PostgreSQL | 5432 | postgresql://localhost:5432 |
| RabbitMQ | 5672 | amqp://localhost:5672 |
| RabbitMQ Admin | 15672 | http://localhost:15672 |
| Redis | 6379 | redis://localhost:6379 |
| **OpenTelemetry - gRPC** | **4317** | **localhost:4317** |
| **OpenTelemetry - HTTP** | **4318** | **http://localhost:4318** |
| **OpenTelemetry - Health** | **13133** | **http://localhost:13133** |
| **OpenTelemetry - ZPages** | **55679** | **http://localhost:55679** |
| **OpenTelemetry - Prometheus** | **8889** | **http://localhost:8889** |
| **Jaeger** | **16686** | **http://localhost:16686** |
| **Zipkin** | **9411** | **http://localhost:9411** |
| **Prometheus** | **9090** | **http://localhost:9090** |
| **Loki** | **3100** | **http://localhost:3100** |
| **Grafana** | **3000** | **http://localhost:3000** |

### Credenciales por Defecto

| Servicio | Usuario | Contraseña |
|----------|---------|-----------|
| PostgreSQL | root | secret |
| RabbitMQ | guest | guest |
| Redis | N/A | N/A |
| Grafana | admin | admin (anonymous enabled) |

---

## Próximos Pasos

1. ✅ Configurar todas las variables en `application.properties`
2. ✅ Levantar infraestructura (Docker Compose unificado)
3. ✅ Implementar servicios de observabilidad (Jaeger, Zipkin, Prometheus, Loki, Grafana)
4. ✅ Integrar OpenTelemetry Collector para recolección centralizada de telemetría
5. ✅ Desplegar en producción (192.168.1.135)
6. 📝 Configurar instrumentación de OpenTelemetry en la aplicación Spring Boot
7. 📝 Configurar dashboards personalizados en Grafana
8. 📝 Agregar autenticación JWT
9. 📝 Implementar validaciones más robustas
10. 📝 Agregar tests unitarios e integración
11. 📝 Configurar CI/CD (GitHub Actions, Jenkins, etc.)
12. 📝 Documentar con Swagger/OpenAPI

---

## Despliegue en Producción

La aplicación está desplegada en **192.168.1.135** en `/opt/CustomerApi`

### Servicios Disponibles

**Aplicación y Base de Datos:**
- **API**: http://192.168.1.135:8080
- **PostgreSQL**: 192.168.1.135:5432
- **RabbitMQ**: 192.168.1.135:5672 (Admin: 15672)
- **Redis**: 192.168.1.135:6379

**OpenTelemetry Collector:**
- **OTLP gRPC**: 192.168.1.135:4317
- **OTLP HTTP**: 192.168.1.135:4318
- **Health Check**: 192.168.1.135:13133
- **ZPages**: 192.168.1.135:55679
- **Prometheus Metrics**: 192.168.1.135:8889

**Observabilidad:**
- **Grafana**: http://192.168.1.135:3000
- **Jaeger**: http://192.168.1.135:16686
- **Zipkin**: http://192.168.1.135:9411
- **Prometheus**: http://192.168.1.135:9090
- **Loki**: http://192.168.1.135:3100

---

## Contacto y Soporte

Para reportar bugs o sugerencias, contacta al equipo de desarrollo.

---

**Última actualización:** 24 de Enero de 2026
**Versión:** 2.1
**Estado:** ✅ Producción (OpenTelemetry Integrado)
