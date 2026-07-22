# Go Channels & Concurrency

This module demonstrates the **Producer-Consumer** pattern in Go using channels, goroutines, and synchronization primitives.

## What are Go Channels?

Channels are the pipes that connect concurrent goroutines. You can send values into channels from one goroutine and receive those values in another goroutine, facilitating safe communication and synchronization without explicit locks or race conditions.

### Core Concepts

1. **Creating Channels**:
   - Unbuffered: `ch := make(chan int)` (blocks sender until receiver is ready)
   - Buffered: `ch := make(chan int, 10)` (does not block sender until buffer is full)

2. **Channel Operations**:
   - Send: `ch <- value`
   - Receive: `value := <-ch`
   - Close: `close(ch)`

3. **Directional Channels**:
   - Send-only: `chan<- T`
   - Receive-only: `<-chan T`

---

## Producer-Consumer Implementation

This example (`main.go`) demonstrates:
- **Multiple Producers**: Generating jobs concurrently.
- **Multiple Consumers (Worker Pool)**: Processing jobs concurrently.
- **Channel Synchronization**: Using `sync.WaitGroup` to coordinate shutdown and close channels safely.
- **Context support**: Leveraging `context.Context` to handle cancellation and timeouts.

### Code Overview

- [main.go](file:///Users/rhishikesh/GITHUB/study-interview-preparation/golang/channels/main.go): Implements the Producer-Consumer workflow.
- [main_test.go](file:///Users/rhishikesh/GITHUB/study-interview-preparation/golang/channels/main_test.go): Unit tests for correctness.

### How to Run

To run the program:
```bash
go run main.go
```

To run the tests:
```bash
go test -v main.go main_test.go
```
