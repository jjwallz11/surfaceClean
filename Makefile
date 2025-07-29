# Makefile at project root (surfaceClean/)
# Handles backend only (app/)

BACKEND_IMAGE=surface-backend
BACKEND_NAME=surface-backend-container
BACKEND_PORT=2911
BACKEND_DIR=app
ENV_FILE=.env

backend-build:
	docker build -t $(BACKEND_IMAGE) -f $(BACKEND_DIR)/Dockerfile $(BACKEND_DIR)

backend-up: backend-build
	docker run -d \
		--name $(BACKEND_NAME) \
		-p $(BACKEND_PORT):$(BACKEND_PORT) \
		--env-file $(ENV_FILE) \
		-v $$(pwd)/$(BACKEND_DIR):/app \
		$(BACKEND_IMAGE)
	sleep 5 && docker exec $(BACKEND_NAME) python seeds/cli.py all || true

backend-down:
	docker stop $(BACKEND_NAME) && docker rm $(BACKEND_NAME)

backend-shell:
	docker exec -it $(BACKEND_NAME) /bin/bash

backend-rebuild: backend-down backend-up

run: backend-up
run-down: backend-down
restart: backend-rebuild