package main

import (
	"sync"
	"testing"
	"time"
)

func TestRunTask(t *testing.T) {
	var wg sync.WaitGroup
	resultsChan := make(chan Task, 1)

	wg.Add(1)
	go runTask(99, 10*time.Millisecond, &wg, resultsChan)

	wg.Wait()
	close(resultsChan)

	result, ok := <-resultsChan
	if !ok {
		t.Fatal("Expected result from channel, but channel was closed empty")
	}

	if result.ID != 99 {
		t.Errorf("Expected ID 99, got %d", result.ID)
	}

	expectedResult := "Result from Task 99 (completed in 10ms)"
	if result.Result != expectedResult {
		t.Errorf("Expected result %q, got %q", expectedResult, result.Result)
	}
}
