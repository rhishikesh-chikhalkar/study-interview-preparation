package main

import (
	"fmt"
	"sync"
	"time"
)

// Task represents a concurrent unit of work.
type Task struct {
	ID       int
	Duration time.Duration
	Result   string
}

// runTask simulates a task execution by sleeping and then sending the result.
func runTask(id int, duration time.Duration, wg *sync.WaitGroup, resultsChan chan<- Task) {
	defer wg.Done() // Signal to the WaitGroup that this goroutine is done when the function exits

	fmt.Printf("[Task %d] Started, will take %v...\n", id, duration)
	time.Sleep(duration) // Simulate work

	result := fmt.Sprintf("Result from Task %d (completed in %v)", id, duration)
	fmt.Printf("[Task %d] Finished!\n", id)

	// Send the result to the buffered channel
	resultsChan <- Task{
		ID:       id,
		Duration: duration,
		Result:   result,
	}
}

func main() {
	fmt.Println("=== Goroutines & Channels Demo ===")

	// 1. Create a channel to communicate results between goroutines.
	// We use a buffered channel of size 3 because we have exactly 3 tasks.
	// This prevents the sender goroutines from blocking on write.
	resultsChan := make(chan Task, 3)

	// 2. Use a sync.WaitGroup to wait for all concurrent goroutines to finish.
	var wg sync.WaitGroup

	// Define 3 tasks with different execution times
	tasks := []struct {
		id       int
		duration time.Duration
	}{
		{id: 1, duration: 800 * time.Millisecond},
		{id: 2, duration: 300 * time.Millisecond},
		{id: 3, duration: 500 * time.Millisecond},
	}

	startTime := time.Now()

	// 3. Launch 3 goroutines concurrently
	for _, t := range tasks {
		wg.Add(1) // Increment the WaitGroup counter for each goroutine
		go runTask(t.id, t.duration, &wg, resultsChan)
	}

	// 4. Wait for all tasks to complete in a separate goroutine and close the channel.
	// Closing the channel tells the receiver loop that no more values will be sent.
	go func() {
		wg.Wait()
		close(resultsChan)
	}()

	// 5. Read the results from the channel as they arrive.
	// This loop will block until a result is sent, and terminate when the channel is closed.
	fmt.Println("\nWaiting for results...")
	for result := range resultsChan {
		fmt.Printf("Received: ID=%d, %s\n", result.ID, result.Result)
	}

	totalDuration := time.Since(startTime)
	fmt.Printf("\nAll tasks completed in: %v (should be close to the maximum duration: 800ms)\n", totalDuration)
}
