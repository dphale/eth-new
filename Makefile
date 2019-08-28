.PHONY: build

build:
	mkdir -p dist
	cp -r src/* dist/
	cp build/contracts/* dist
