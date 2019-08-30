.PHONY: build

build:
	mkdir -p dist/vendor
	cp -r src/* dist/
	cp build/contracts/* dist
	cp -r node_modules/* dist/vendor

start:
	docker-compose build
	docker-compose up --force-recreate
