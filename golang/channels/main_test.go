package main

import (
	"context"
	"sync"
	"testing"
	"time"
)

func TestProducerConsumer(t *testing.T) {
	jobsChan := make(chan Job, 10)
	resultsChan := make(chan Result, 10)

	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	var producersWg sync.WaitGroup
	var consumersWg sync.WaitGroup

	// Start 1 producer creating 5 jobs
	producersWg.Add(1)
	go Produce(ctx, 1, jobsChan, 5, &producersWg)

	// Start 1 consumer
	consumersWg.Add(1)
	go Consume(ctx, 1, jobsChan, resultsChan, &consumersWg)

	// Close jobsChan when producer is done
	go func() {
		producersWg.Wait()
		close(jobsChan)
	}()

	// Close resultsChan when consumer is done
	go func() {
		consumersWg.Wait()
		close(resultsChan)
	}()

	// Gather results
	resultsCount := 0
	for result := range resultsChan {
		resultsCount++
		if !result.Processed {
			t.Errorf("Expected result to be processed")
		}
		if result.WorkerID != 1 {
			t.Errorf("Expected WorkerID to be 1, got %d", result.WorkerID)
		}
	}

	if resultsCount != 5 {
		t.Errorf("Expected 5 results, got %d", resultsCount)
	}
}
