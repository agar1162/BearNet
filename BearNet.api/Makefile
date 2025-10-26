.PHONY: dev prod down logs

dev:
	./mvnw clean package
	docker compose -f docker-compose.dev.yaml down --remove-orphans
	docker compose -f docker-compose.dev.yaml up --build -d

prod:
	./mvnw clean package
	docker compose -f docker-compose.prod.yaml down --remove-orphans
	docker compose -f docker-compose.prod.yaml up --build -d

down:
	docker compose -f docker-compose.dev.yaml down --remove-orphans || \
	docker compose -f docker-compose.prod.yaml down --remove-orphans

logs:
	docker compose logs -f