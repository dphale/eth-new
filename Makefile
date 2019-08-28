.PHONY: build

truffle:
	truffle compile
	truffle migrate

build: truffle
	mkdir -p dist/vendor
	cp -r src/* dist/
	cp build/contracts/* dist
	cp -r node_modules/* dist/vendor
