.PHONY: run test build docker-build clean

run:
	go run ./cmd/api

test:
	go test -v -race ./...

build:
	go build -ldflags="-w -s" -o bin/api ./cmd/api

docker-build:
	docker build -t render-go-service:latest .

clean:
	rm -rf bin/
