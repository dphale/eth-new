.PHONY: deps build build-docker run

deps:
	mkdir -p /rinkeby/chaindata/keystore
	mkdir -p /rinkeby/passwords
	cp keystore/wallets/* /rinkeby/chaindata/keystore
	cp keystore/passwords/* /rinkeby/passwords/

build:
	mkdir -p dist/vendor
	cp -r src/* dist/
	cp build/contracts/* dist
	cp -r node_modules/* dist/vendor

build-docker:
	docker-compose build

run: build-docker deps
	docker-compose up -d --force-recreate
