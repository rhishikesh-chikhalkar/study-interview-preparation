package main

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// Job represents a unit of work sent from producer to consumer.
type Job struct {
	ID        int
	Payload   int
	CreatedAt time.Time
}

// Result represents the outcome of processing a Job.
type Result struct {
	Job        Job
	WorkerID   int
	Processed  bool
	Duration   time.Duration
	FinishedAt time.Time
}

// Produce generates jobs and sends them to the jobs channel.
func Produce(ctx context.Context, id int, jobsChan chan<- Job, count int, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 1; i <= count; i++ {
		select {
		case <-ctx.Done():
			fmt.Printf("[Producer %d] Stopped due to cancellation\n", id)
			return
		default:
			job := Job{
				ID:        (id * 1000) + i,
				Payload:   rand.Intn(100),
				CreatedAt: time.Now(),
			}
			fmt.Printf("[Producer %d] Created Job %d with payload %d\n", id, job.ID, job.Payload)
			
			// Send the job to the channel (blocks if the channel buffer is full)
			select {
			case jobsChan <- job:
				// Successfully sent
			case <-ctx.Done():
				fmt.Printf("[Producer %d] Stopped while trying to send Job %d\n", id, job.ID)
				return
			}
			
			// Simulate variable production time
			time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
		}
	}
	fmt.Printf("[Producer %d] Finished producing all %d jobs\n", id, count)
}

// Consume processes jobs from the jobs channel and sends results to the results channel.
func Consume(ctx context.Context, id int, jobsChan <-chan Job, resultsChan chan<- Result, wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case <-ctx.Done():
			fmt.Printf("[Consumer %d] Stopped due to cancellation\n", id)
			return
		case job, ok := <-jobsChan:
			if !ok {
				// Channel closed, no more jobs to process
				fmt.Printf("[Consumer %d] No more jobs. Exiting.\n", id)
				return
			}
			
			fmt.Printf("[Consumer %d] Started processing Job %d...\n", id, job.ID)
			
			// Simulate processing time
			processingTime := time.Duration(100+rand.Intn(150)) * time.Millisecond
			time.Sleep(processingTime)
			
			result := Result{
				Job:        job,
				WorkerID:   id,
				Processed:  true,
				Duration:   processingTime,
				FinishedAt: time.Now(),
			}
			
			fmt.Printf("[Consumer %d] Finished Job %d in %v\n", id, job.ID, processingTime)
			
			select {
			case resultsChan <- result:
				// Successfully sent result
			case <-ctx.Done():
				fmt.Printf("[Consumer %d] Stopped while trying to send result for Job %d\n", id, job.ID)
				return
			}
		}
	}
}

func main() {
	// Seed random number generator
	rand.Seed(time.Now().UnixNano())

	fmt.Println("=== Producer-Consumer Concurrency Pattern with Go Channels ===")

	// Channels definition
	// We use a buffered channel of size 5 for jobs to allow producers to work slightly ahead.
	jobsChan := make(chan Job, 5)
	resultsChan := make(chan Result, 20)

	// Context for graceful shutdown/cancellation support
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// WaitGroups for coordination
	var producersWg sync.WaitGroup
	var consumersWg sync.WaitGroup

	numProducers := 2
	numConsumers := 3
	jobsPerProducer := 5

	// Start Producers
	for i := 1; i <= numProducers; i++ {
		producersWg.Add(1)
		go Produce(ctx, i, jobsChan, jobsPerProducer, &producersWg)
	}

	// Start Consumers
	for i := 1; i <= numConsumers; i++ {
		consumersWg.Add(1)
		go Consume(ctx, i, jobsChan, resultsChan, &consumersWg)
	}

	// Orchestrator: Close jobs channel once all producers are done.
	// This signals consumers that no more jobs are coming.
	go func() {
		producersWg.Wait()
		fmt.Println("[Orchestrator] All producers finished. Closing jobs channel.")
		close(jobsChan)
	}()

	// Orchestrator: Close results channel once all consumers are done.
	go func() {
		consumersWg.Wait()
		fmt.Println("[Orchestrator] All consumers finished. Closing results channel.")
		close(resultsChan)
	}()

	// Read results from the results channel
	totalJobsProcessed := 0
	for result := range resultsChan {
		totalJobsProcessed++
		fmt.Printf("[Main] Received Result: Job %d processed by Consumer %d in %v\n", 
			result.Job.ID, result.WorkerID, result.Duration)
	}

	fmt.Printf("\nProcessing complete. Total jobs processed: %d\n", totalJobsProcessed)
}
