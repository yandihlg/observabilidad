# 🚀 GUÍA DE INICIO RÁPIDO

## Opción 1: Automatizado (RECOMENDADO)

### Un comando lo hace TODO:
```bash
python3 setup_and_test.py
```

**¿Qué hace?**
- ✅ Detiene contenedores previos
- ✅ Levanta 10 servicios Docker
- ✅ Espera inicialización (máx 120s)
- ✅ Verifica que funcionen
- ✅ Ejecuta 5 pruebas de API (GET, POST, PUT, DELETE)
- ✅ Genera logs estructurados
- ✅ Muestra resultados en tablas
- ✅ Proporciona URLs de acceso

**Salida esperada:**
```
================================================================================
                    CUSTOMER API - SETUP Y TEST AUTOMATIZADO
================================================================================

✓ Todos los contenedores están en ejecución
✓ customer-api respondiendo correctamente
...

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

4. Jaeger
   🔗 http://localhost:16686
   📝 Visualizador de Trazas

5. Loki
   🔗 http://localhost:3100
   📝 Almacenamiento de Logs
   
...
```

---

## Opción 2: Manual (Paso a paso)

### Paso 1: Detener contenedores previos
```bash
docker-compose down
```

### Paso 2: Levantar contenedores
```bash
docker-compose up -d
```

### Paso 3: Esperar a que se inicialicen
```bash
# Verificar estado
docker-compose ps

# O esperar con:
docker-compose up -d && sleep 30
```

### Paso 4: Probar manualmente
```bash
# GET todos los clientes
curl -s http://localhost:8080/api/customer | jq

# POST crear cliente
curl -s -X POST http://localhost:8080/api/customer \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Juan",
    "lastName": "Perez",
    "phone": "555-1234",
    "age": 30,
    "birthDate": "1993-05-15",
    "address": "Calle Principal",
    "city": "Madrid",
    "country": "Spain"
  }'
```

### Paso 5: Ver logs
```bash
# Logs de la API
docker logs customer-api | tail -50

# Logs en formato JSON
docker logs customer-api | grep "trace_id" | tail -10
```

---

## 📍 URLs DE ACCESO

### Desarrollo (localhost)

| Servicio | URL |
|----------|-----|
| API | http://localhost:8080/api/customer |
| Grafana | http://localhost:3000 (admin/admin) |
| Prometheus | http://localhost:9090 |
| Jaeger | http://localhost:16686 |
| Loki | http://localhost:3100 |
| Zipkin | http://localhost:9411 |
| RabbitMQ | http://localhost:15672 (guest/guest) |

---

## 🔍 PRÓXIMOS PASOS DESPUÉS DE LEVANTAR

### 1. Ver Trazas en Jaeger
```
1. Abre http://localhost:16686
2. Selecciona "customer-api" en el dropdown
3. Busca operaciones como "http.get.findAll"
4. Haz clic para ver detalles de la traza
```

### 2. Ver Logs en Grafana
```
1. Abre http://localhost:3000 (admin/admin)
2. Ve a "Explore" > "Loki"
3. Escribe: {service_name="customer-api"}
4. Verás logs estructurados con trace IDs
```

### 3. Ver Métricas en Prometheus
```
1. Abre http://localhost:9090
2. Busca métrica: http_server_request_duration_seconds
3. Visualiza gráficos de rendimiento
```

### 4. Hacer más pruebas
```bash
# En un terminal, ejecutar pruebas continuamente
while true; do
  curl -s http://localhost:8080/api/customer | jq '.[] | .firstName, .lastName' | head -5
  sleep 2
done

# Luego en Grafana, verás los logs actualizándose en tiempo real
```

---

## 🐛 TROUBLESHOOTING RÁPIDO

### Los contenedores no levantan
```bash
# Ver errores
docker-compose logs

# Limpiar y reintentar
docker-compose down -v
docker-compose up -d
```

### API no responde
```bash
# Verificar si está corriendo
docker ps | grep customer-api

# Ver logs de la aplicación
docker logs customer-api

# Esperar más tiempo (puede tomar 30-60s en primera ejecución)
sleep 30
curl http://localhost:8080/api/customer
```

### PostgreSQL tiene problemas de conexión
```bash
# Verificar logs de la BD
docker logs customer-db

# Resetear base de datos
docker-compose down -v
docker-compose up -d customer-db
```

### Loki no muestra logs
```bash
# Verificar que el collector está recibiendo logs
docker logs customer-otel-collector | grep -i "loki"

# Esperar a que se procesen (pueden tardar unos segundos)
sleep 5

# Hacer una nueva petición a la API
curl http://localhost:8080/api/customer

# Intentar consultar nuevamente en Grafana
```

---

## 📊 INFORMACIÓN TÉCNICA

| Componente | Versión | Puerto |
|-----------|---------|--------|
| Java | 21 LTS | - |
| Spring Boot | 3.2.0 | 8080 |
| OpenTelemetry | 2.4.0 | 4317 (gRPC) |
| PostgreSQL | 14+ | 5432 |
| Redis | 7+ | 6379 |
| RabbitMQ | 3.13+ | 5672 |
| Prometheus | latest | 9090 |
| Grafana | latest | 3000 |
| Jaeger | latest | 16686 |
| Loki | latest | 3100 |

---

## 📝 DOCUMENTACIÓN COMPLETA

Para más detalles, ver: [README.md](README.md)

- Stack Tecnológico completo
- Arquitectura de Observabilidad
- Instrumentación manual de OTEL
- Configuración de Docker Compose
- Endpoints de la API
- Solución de problemas avanzada

---

## ✨ CARACTERÍSTICAS PRINCIPALES

✅ **Observabilidad Completa**
- Trazas distribuidas (Jaeger)
- Métricas en tiempo real (Prometheus)
- Logs estructurados (Loki)
- Dashboard unificado (Grafana)

✅ **Instrumentación Automática**
- OpenTelemetry Java Agent v2.4.0
- Captura automática de HTTP, DB, mensajes
- Correlación de trazas

✅ **APIs REST Completas**
- CRUD de clientes
- Manejo de errores
- Validaciones

✅ **Infrastructure as Code**
- Docker Compose unificado
- 10 servicios configurados
- Fácil de desplegar

---

**¿Listo para empezar?**

```bash
python3 setup_and_test.py
```

¡Disfruta de tu sistema de observabilidad! 🎉
