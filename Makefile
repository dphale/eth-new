.PHONY: deps build run

deps:
	mkdir -p /rinkeby/chaindata/keystore
	mkdir -p /rinkeby/passwords
	cp keystore/wallets/* /rinkeby/chaindata/keystore
	cp keystore/passwords/* /rinkeby/passwords/

build:
	docker-compose build

run: build deps
	docker-compose up --force-recreate
