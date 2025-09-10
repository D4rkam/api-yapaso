# Makefile para Ya Paso API
# Comandos comunes para desarrollo y despliegue

.PHONY: help install dev test clean docker-build docker-run docker-down lint format

# Configuración por defecto
PYTHON := python3
PIP := pip3
UVICORN := uvicorn
DOCKER_COMPOSE := docker-compose

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
	$(PIP) install -r requirements.txt

install-dev: ## Instalar dependencias de desarrollo
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy

dev: ## Ejecutar servidor de desarrollo
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

dev-debug: ## Ejecutar servidor con debug habilitado
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

test: ## Ejecutar tests
	pytest tests/ -v

test-cov: ## Ejecutar tests con cobertura
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

lint: ## Verificar código con linters
	flake8 app/
	mypy app/

format: ## Formatear código
	black app/
	black tests/

format-check: ## Verificar formato sin modificar
	black --check app/
	black --check tests/

clean: ## Limpiar archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/

# Comandos Docker
docker-build: ## Construir imagen Docker
	docker build -t yapaso-api .

docker-run: ## Ejecutar contenedor individual
	docker run -p 8000:8000 --name yapaso-api-container yapaso-api

docker-up: ## Levantar todos los servicios con docker-compose
	$(DOCKER_COMPOSE) up -d

docker-up-dev: ## Levantar servicios incluye phpMyAdmin para desarrollo
	$(DOCKER_COMPOSE) --profile development up -d

docker-down: ## Detener todos los servicios
	$(DOCKER_COMPOSE) down

docker-logs: ## Ver logs de los servicios
	$(DOCKER_COMPOSE) logs -f

docker-shell: ## Acceder al shell del contenedor de la API
	$(DOCKER_COMPOSE) exec api sh

docker-db-shell: ## Acceder al shell de MySQL
	$(DOCKER_COMPOSE) exec mysql mysql -u yapaso_user -pyapaso_password yapaso_db

# Comandos de base de datos
db-reset: ## Resetear base de datos (solo en desarrollo)
	@echo "¿Estás seguro de que quieres resetear la base de datos? [y/N]" && read ans && [ $${ans:-N} = y ]
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) up -d mysql
	sleep 10
	$(DOCKER_COMPOSE) up -d api

# Comandos de despliegue
deploy-staging: ## Desplegar a staging
	@echo "Desplegando a staging..."
	# TODO: Agregar comandos de despliegue

deploy-prod: ## Desplegar a producción
	@echo "Desplegando a producción..."
	# TODO: Agregar comandos de despliegue

# Comandos de desarrollo
check: lint test ## Ejecutar todas las verificaciones

setup-dev: install-dev ## Configurar entorno de desarrollo completo
	cp app/.env.example app/.env
	@echo "✅ Entorno de desarrollo configurado"
	@echo "📝 Edita app/.env con tus configuraciones"
	@echo "🚀 Ejecuta 'make docker-up-dev' para iniciar"

status: ## Mostrar estado de los servicios
	$(DOCKER_COMPOSE) ps

# Comandos de utilidad
generate-secret: ## Generar clave secreta
	$(PYTHON) -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

deps-update: ## Actualizar dependencias
	$(PIP) list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 $(PIP) install -U

backup-db: ## Hacer backup de la base de datos
	@echo "Creando backup de base de datos..."
	$(DOCKER_COMPOSE) exec -T mysql mysqldump -u yapaso_user -pyapaso_password yapaso_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup creado: backup_$(shell date +%Y%m%d_%H%M%S).sql"