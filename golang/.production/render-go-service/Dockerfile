# Stage 1: Build static Go binary
FROM golang:1.25-alpine AS builder

WORKDIR /app

RUN apk add --no-cache ca-certificates tzdata

COPY go.mod ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-w -s" \
    -o /app/bin/api ./cmd/api

# Stage 2: Minimal runtime image
FROM alpine:latest

WORKDIR /app

RUN apk upgrade --no-cache && addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /app/bin/api /app/api

USER appuser

EXPOSE 8080

ENTRYPOINT ["/app/api"]
