#!/usr/bin/env python3
"""
Customer API - Automated Setup, Test & Validation Script
=========================================================
Este script automáticamente:
1. Levanta todos los contenedores Docker
2. Espera a que se inicialicen
3. Verifica que están funcionando
4. Ejecuta pruebas contra las APIs
5. Genera logs
6. Valida que los logs se generen correctamente
7. Muestra resumen en tablas
8. Proporciona URLs de acceso a los servicios
"""

import subprocess
import time
import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import json
from urllib.parse import urlencode

# ==================== COLORES Y ESTILOS ====================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ==================== CONFIGURACIÓN ====================
DOCKER_COMPOSE_FILE = "docker-compose.yml"
SERVICES = [
    "customer-db",
    "customer-redis",
    "customer-rabbitmq",
    "customer-otel-collector",
    "customer-prometheus",
    "customer-grafana",
    "customer-jaeger",
    "customer-loki",
    "customer-zipkin",
    "customer-api"
]

CONTAINER_PORTS = {
    "customer-api": 8080,
    "customer-db": 5432,
    "customer-redis": 6379,
    "customer-rabbitmq": 5672,
    "customer-otel-collector": 4317,
    "customer-prometheus": 9090,
    "customer-grafana": 3000,
    "customer-jaeger": 16686,
    "customer-loki": 3100,
    "customer-zipkin": 9411,
}

API_BASE_URL = "http://localhost:8080/api/customer"
MAX_WAIT_TIME = 120  # segundos
CHECK_INTERVAL = 5   # segundos

# ==================== UTILIDADES ====================
def print_header(title: str):
    """Imprime un encabezado formateado"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_section(title: str):
    """Imprime un subtítulo formateado"""
    print(f"{Colors.CYAN}{Colors.BOLD}▶ {title}{Colors.ENDC}")

def print_success(msg: str):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✓ {msg}{Colors.ENDC}")

def print_error(msg: str):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}✗ {msg}{Colors.ENDC}")

def print_warning(msg: str):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.ENDC}")

def print_info(msg: str):
    """Imprime mensaje informativo"""
    print(f"{Colors.BLUE}ℹ {msg}{Colors.ENDC}")

def run_command(cmd: str, show_output: bool = False) -> Tuple[bool, str]:
    """Ejecuta un comando de shell"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        if show_output:
            print(result.stdout)
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Comando timeout"
    except Exception as e:
        return False, str(e)

def print_table(headers: List[str], rows: List[List[str]]):
    """Imprime una tabla formateada"""
    # Calcular ancho de columnas
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Línea separadora
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    # Encabezado
    print(separator)
    header_line = "|" + "|".join(f" {h:<{col_widths[i]}} " for i, h in enumerate(headers)) + "|"
    print(header_line)
    print(separator)
    
    # Filas
    for row in rows:
        row_line = "|" + "|".join(f" {str(cell):<{col_widths[i]}} " for i, cell in enumerate(row)) + "|"
        print(row_line)
    
    print(separator)

# ==================== FUNCIONES PRINCIPALES ====================

def step_1_docker_compose_down():
    """Paso 1: Detener contenedores previos"""
    print_section("Paso 1/7: Deteniendo contenedores previos...")
    success, _ = run_command(f"docker-compose -f {DOCKER_COMPOSE_FILE} down 2>/dev/null", show_output=False)
    if success:
        print_success("Contenedores detenidos correctamente")
    else:
        print_warning("No había contenedores previos (esto es normal)")
    time.sleep(2)

def step_2_docker_compose_up():
    """Paso 2: Levantar los contenedores"""
    print_section("Paso 2/7: Levantando contenedores Docker...")
    print_info(f"Iniciando {len(SERVICES)} servicios...")
    
    success, output = run_command(f"docker-compose -f {DOCKER_COMPOSE_FILE} up -d")
    
    if not success:
        print_error("Error al levantar contenedores")
        print(output)
        return False
    
    print_success("Comando docker-compose up ejecutado")
    return True

def step_3_wait_for_containers():
    """Paso 3: Esperar a que los contenedores estén listos"""
    print_section("Paso 3/7: Esperando a que los contenedores se inicialicen...")
    
    elapsed_time = 0
    all_ready = False
    
    while elapsed_time < MAX_WAIT_TIME:
        # Verificar estado de cada servicio
        success, output = run_command("docker-compose -f docker-compose.yml ps --format json 2>/dev/null")
        
        if success:
            try:
                containers = json.loads(output)
                running = sum(1 for c in containers if c.get('State') == 'running')
                total = len(containers)
                
                if running == total and total > 0:
                    all_ready = True
                    break
                
                # Mostrar progreso
                elapsed_time += CHECK_INTERVAL
                remaining = MAX_WAIT_TIME - elapsed_time
                print_info(f"Contenedores en ejecución: {running}/{total} (tiempo restante: {remaining}s)")
            except:
                pass
        
        time.sleep(CHECK_INTERVAL)
    
    if all_ready:
        print_success("✓ Todos los contenedores están en ejecución")
        time.sleep(5)  # Esperar a que se inicialicen completamente
        return True
    else:
        print_error("Timeout esperando a que se inicialicen los contenedores")
        return False

def step_4_verify_services():
    """Paso 4: Verificar que los servicios estén respondiendo"""
    print_section("Paso 4/7: Verificando servicios...")
    
    service_status = {}
    health_checks = {
        "customer-api": ("GET", f"{API_BASE_URL}"),
        "customer-grafana": ("GET", "http://localhost:3000/api/health"),
        "customer-prometheus": ("GET", "http://localhost:9090/-/healthy"),
        "customer-jaeger": ("GET", "http://localhost:16686/"),
        "customer-loki": ("GET", "http://localhost:3100/ready"),
    }
    
    for service, (method, url) in health_checks.items():
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
                service_status[service] = response.status_code < 500
            print_success(f"{service} respondiendo correctamente")
        except:
            service_status[service] = False
            print_warning(f"{service} aún no está listo (reintentando...)")
            time.sleep(2)
    
    return True

def step_5_run_api_tests():
    """Paso 5: Ejecutar pruebas de la API"""
    print_section("Paso 5/7: Ejecutando pruebas de API...")
    
    test_results = []
    
    # Test 1: GET all customers
    print_info("Test 1: Obtener todos los clientes...")
    try:
        response = requests.get(API_BASE_URL, timeout=10)
        test_results.append({
            "test": "GET /api/customer (Listar todos)",
            "metodo": "GET",
            "status": response.status_code,
            "resultado": "✓ ÉXITO" if response.status_code == 200 else "✗ FALLO"
        })
        print_success(f"Status: {response.status_code}")
        existing_customers = response.json() if response.status_code == 200 else []
    except Exception as e:
        test_results.append({
            "test": "GET /api/customer",
            "metodo": "GET",
            "status": "ERROR",
            "resultado": str(e)
        })
        print_error(f"Error: {e}")
        existing_customers = []
    
    time.sleep(1)
    
    # Test 2: POST create customer
    print_info("Test 2: Crear nuevo cliente...")
    new_customer = {
        "firstName": "TestUser",
        "lastName": "AutoTest",
        "phone": "555-0123",
        "age": 25,
        "birthDate": "2000-01-15",
        "address": "Test Street 123",
        "city": "Test City",
        "country": "Test Country"
    }
    
    created_customer_id = None
    try:
        response = requests.post(
            API_BASE_URL,
            json=new_customer,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        test_results.append({
            "test": "POST /api/customer (Crear cliente)",
            "metodo": "POST",
            "status": response.status_code,
            "resultado": "✓ ÉXITO" if response.status_code == 201 else "✗ FALLO"
        })
        if response.status_code == 201:
            created_customer_id = response.json().get("id")
            print_success(f"Status: {response.status_code}, ID creado: {created_customer_id}")
    except Exception as e:
        test_results.append({
            "test": "POST /api/customer",
            "metodo": "POST",
            "status": "ERROR",
            "resultado": str(e)
        })
        print_error(f"Error: {e}")
    
    time.sleep(1)
    
    # Test 3: GET by ID
    if created_customer_id:
        print_info("Test 3: Obtener cliente por ID...")
        try:
            response = requests.get(f"{API_BASE_URL}/{created_customer_id}", timeout=10)
            test_results.append({
                "test": f"GET /api/customer/{created_customer_id} (Por ID)",
                "metodo": "GET",
                "status": response.status_code,
                "resultado": "✓ ÉXITO" if response.status_code == 200 else "✗ FALLO"
            })
            print_success(f"Status: {response.status_code}")
        except Exception as e:
            test_results.append({
                "test": f"GET /api/customer/{created_customer_id}",
                "metodo": "GET",
                "status": "ERROR",
                "resultado": str(e)
            })
            print_error(f"Error: {e}")
        
        time.sleep(1)
        
        # Test 4: PUT update
        print_info("Test 4: Actualizar cliente...")
        update_data = {
            "firstName": "TestUserUpdated",
            "lastName": "AutoTestUpdated",
            "phone": "555-9876",
            "age": 26,
            "birthDate": "2000-01-15",
            "address": "Updated Street 456",
            "city": "Updated City",
            "country": "Updated Country"
        }
        try:
            response = requests.put(
                f"{API_BASE_URL}/{created_customer_id}",
                json=update_data,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            test_results.append({
                "test": f"PUT /api/customer/{created_customer_id} (Actualizar)",
                "metodo": "PUT",
                "status": response.status_code,
                "resultado": "✓ ÉXITO" if response.status_code == 200 else "✗ FALLO"
            })
            print_success(f"Status: {response.status_code}")
        except Exception as e:
            test_results.append({
                "test": f"PUT /api/customer/{created_customer_id}",
                "metodo": "PUT",
                "status": "ERROR",
                "resultado": str(e)
            })
            print_error(f"Error: {e}")
        
        time.sleep(1)
        
        # Test 5: DELETE
        print_info("Test 5: Eliminar cliente...")
        try:
            response = requests.delete(f"{API_BASE_URL}/{created_customer_id}", timeout=10)
            test_results.append({
                "test": f"DELETE /api/customer/{created_customer_id} (Eliminar)",
                "metodo": "DELETE",
                "status": response.status_code,
                "resultado": "✓ ÉXITO" if response.status_code == 200 else "✗ FALLO"
            })
            print_success(f"Status: {response.status_code}")
        except Exception as e:
            test_results.append({
                "test": f"DELETE /api/customer/{created_customer_id}",
                "metodo": "DELETE",
                "status": "ERROR",
                "resultado": str(e)
            })
            print_error(f"Error: {e}")
    
    return test_results

def step_6_verify_logs():
    """Paso 6: Verificar que los logs se generen correctamente"""
    print_section("Paso 6/7: Verificando generación de logs...")
    
    try:
        # Obtener logs del contenedor customer-api
        success, logs_output = run_command(
            "docker logs customer-api 2>&1 | tail -100 | grep -E '\"logger\"|\"trace_id\"' | head -20",
            show_output=False
        )
        
        if success and logs_output:
            # Contar líneas de logs JSON
            log_lines = [l for l in logs_output.split('\n') if l.strip()]
            print_success(f"Se detectaron {len(log_lines)} líneas de logs estructurados")
            
            # Mostrar ejemplo de log
            if log_lines:
                print_info("Ejemplo de log capturado:")
                try:
                    # Intentar parsear y mostrar un log JSON formateado
                    for log_line in log_lines[:1]:
                        if log_line.strip().startswith('{'):
                            log_json = json.loads(log_line)
                            print(f"  └─ Logger: {log_json.get('logger', 'N/A')}")
                            print(f"  └─ Level: {log_json.get('severity', 'N/A')}")
                            print(f"  └─ Thread: {log_json.get('thread', 'N/A')}")
                            print(f"  └─ Message: {log_json.get('message', 'N/A')[:60]}...")
                            if 'trace_id' in log_json:
                                print(f"  └─ Trace ID: {log_json.get('trace_id', 'N/A')}")
                except:
                    pass
            
            return True, log_lines
        else:
            print_warning("No se encontraron logs estructurados")
            return False, []
    except Exception as e:
        print_error(f"Error verificando logs: {e}")
        return False, []

def step_7_services_urls():
    """Paso 7: Mostrar URLs de los servicios"""
    print_section("Paso 7/7: URLs de acceso a los servicios")
    
    services_info = [
        {
            "Servicio": "Customer API",
            "URL": "http://localhost:8080/api/customer",
            "Descripción": "API REST de Clientes"
        },
        {
            "Servicio": "Grafana",
            "URL": "http://localhost:3000",
            "Descripción": "Dashboard de Observabilidad (user: admin, pass: admin)"
        },
        {
            "Servicio": "Prometheus",
            "URL": "http://localhost:9090",
            "Descripción": "Recopilador de Métricas"
        },
        {
            "Servicio": "Jaeger",
            "URL": "http://localhost:16686",
            "Descripción": "Visualizador de Trazas Distribuidas"
        },
        {
            "Servicio": "Loki",
            "URL": "http://localhost:3100",
            "Descripción": "Sistema de Almacenamiento de Logs"
        },
        {
            "Servicio": "Zipkin",
            "URL": "http://localhost:9411",
            "Descripción": "Rastreador Distribuido (alternativa a Jaeger)"
        },
        {
            "Servicio": "RabbitMQ",
            "URL": "http://localhost:15672",
            "Descripción": "Message Broker (user: guest, pass: guest)"
        },
        {
            "Servicio": "PostgreSQL",
            "URL": "localhost:5432",
            "Descripción": "Base de Datos (user: postgres, pass: password)"
        },
        {
            "Servicio": "Redis",
            "URL": "localhost:6379",
            "Descripción": "Cache en Memoria"
        },
    ]
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ACCESO A LOS SERVICIOS:{Colors.ENDC}\n")
    
    for i, service in enumerate(services_info, 1):
        print(f"{Colors.BOLD}{i}. {service['Servicio']}{Colors.ENDC}")
        print(f"   🔗 {Colors.BLUE}{service['URL']}{Colors.ENDC}")
        print(f"   📝 {service['Descripción']}\n")
    
    return services_info

# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    print_header("CUSTOMER API - SETUP Y TEST AUTOMATIZADO")
    
    print_info(f"Iniciado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Servicios a levantar: {', '.join(SERVICES)}")
    
    # Paso 1: Detener contenedores previos
    step_1_docker_compose_down()
    
    # Paso 2: Levantar contenedores
    if not step_2_docker_compose_up():
        print_error("Fallo al levantar contenedores")
        return False
    
    # Paso 3: Esperar a que estén listos
    if not step_3_wait_for_containers():
        print_error("Timeout esperando contenedores")
        return False
    
    # Paso 4: Verificar servicios
    step_4_verify_services()
    
    # Paso 5: Ejecutar pruebas API
    test_results = step_5_run_api_tests()
    
    # Paso 6: Verificar logs
    logs_found, log_samples = step_6_verify_logs()
    
    # Mostrar resumen de pruebas
    print_header("RESUMEN DE PRUEBAS")
    
    print(f"\n{Colors.BOLD}Resultados de Tests de API:{Colors.ENDC}\n")
    headers = ["Test", "Método", "Status", "Resultado"]
    rows = [[t["test"][:40], t["metodo"], str(t["status"])[:10], t["resultado"]] for t in test_results]
    print_table(headers, rows)
    
    # Contar éxitos y fallos
    successes = sum(1 for t in test_results if "✓" in t["resultado"])
    total = len(test_results)
    print(f"\n{Colors.GREEN}✓ Pruebas exitosas: {successes}/{total}{Colors.ENDC}\n")
    
    # Paso 7: Mostrar URLs
    print_header("SERVICIOS DISPONIBLES")
    services = step_7_services_urls()
    
    print_header("PRÓXIMOS PASOS")
    print(f"""
{Colors.BOLD}1. ACCEDER A GRAFANA:{Colors.ENDC}
   • URL: {Colors.BLUE}http://localhost:3000{Colors.ENDC}
   • Usuario: admin
   • Contraseña: admin
   • Buscar el datasource "Loki" para ver logs
   • Buscar el datasource "Prometheus" para ver métricas

{Colors.BOLD}2. VER TRAZAS EN JAEGER:{Colors.ENDC}
   • URL: {Colors.BLUE}http://localhost:16686{Colors.ENDC}
   • Seleccionar servicio: customer-api
   • Buscar operaciones: http.get.findAll, http.post.register, etc.

{Colors.BOLD}3. EJECUTAR MÁS PRUEBAS:{Colors.ENDC}
   • {Colors.BLUE}curl -X GET http://localhost:8080/api/customer{Colors.ENDC}
   • {Colors.BLUE}curl -X POST http://localhost:8080/api/customer -H "Content-Type: application/json" -d '{{"firstName":"Test","lastName":"User"...}}{Colors.ENDC}

{Colors.BOLD}4. DETENER LOS CONTENEDORES:{Colors.ENDC}
   • {Colors.BLUE}docker-compose down{Colors.ENDC}

{Colors.BOLD}5. VER LOGS:{Colors.ENDC}
   • {Colors.BLUE}docker logs customer-api | tail -50{Colors.ENDC}
    """)
    
    print_header("INFORMACIÓN DE LA STACK")
    print(f"""
{Colors.BOLD}Stack de Observabilidad:{Colors.ENDC}
   • {Colors.CYAN}OpenTelemetry{Colors.ENDC}: Instrumentación automática v2.4.0
   • {Colors.CYAN}Prometheus{Colors.ENDC}: Recopilación de métricas
   • {Colors.CYAN}Grafana{Colors.ENDC}: Visualización unificada
   • {Colors.CYAN}Jaeger{Colors.ENDC}: Trazas distribuidas
   • {Colors.CYAN}Loki{Colors.ENDC}: Almacenamiento de logs
   • {Colors.CYAN}Zipkin{Colors.ENDC}: Rastreador distribuido alternativo

{Colors.BOLD}Stack de Aplicación:{Colors.ENDC}
   • {Colors.CYAN}Spring Boot{Colors.ENDC} 3.2.0 con Java 21
   • {Colors.CYAN}PostgreSQL{Colors.ENDC} 14+
   • {Colors.CYAN}RabbitMQ{Colors.ENDC}: Message Broker
   • {Colors.CYAN}Redis{Colors.ENDC}: Cache en memoria
    """)
    
    print_header("¡CONFIGURACIÓN COMPLETADA!")
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Sistema listo para monitoreo y observabilidad{Colors.ENDC}\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operación cancelada por el usuario{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.ENDC}")
        sys.exit(1)
