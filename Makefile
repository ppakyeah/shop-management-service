.PHONY: build up down logs ps exec-app clean test format restart help

build:
	docker-compose build web_app_db django_backend

up:
	docker-compose up -d web_app_db django_backend

down:
	docker-compose down

logs:
	docker-compose logs -f

ps:
	docker-compose ps

# 코드 포맷팅
format:
	black .
	isort .

# 컨테이너 접속
exec-app:
	docker-compose exec django_backend bash

test:
	docker-compose up -d web_app_db
	docker-compose run --rm test
	docker-compose stop web_app_db

# 초기화 및 정리
clean:
	docker-compose down -v --remove-orphans

# 개발 환경 시작
dev: build up
	docker-compose logs -f django_backend

# 전체 재시작
restart: down up
	docker-compose logs -f django_backend

# 도움말
help:
	@echo "사용 가능한 명령어:"
	@echo "  make build        - 도커 이미지 빌드"
	@echo "  make up           - 컨테이너 시작"
	@echo "  make down         - 컨테이너 중지"
	@echo "  make logs         - 로그 보기"
	@echo "  make ps           - 실행 중인 컨테이너 목록"
	@echo "  make format       - 코드 포맷팅 실행 (black, isort)"
	@echo "  make exec-app     - 애플리케이션 컨테이너 접속"
	@echo "  make test         - 테스트 실행"
	@echo "  make clean        - 모든 컨테이너 및 볼륨 제거"
	@echo "  make dev          - 개발 환경 시작"
	@echo "  make restart      - 전체 재시작"