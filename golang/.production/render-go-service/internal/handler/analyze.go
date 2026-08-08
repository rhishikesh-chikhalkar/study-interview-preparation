package handler

import (
	"encoding/json"
	"net/http"
	"strings"
	"time"
)

type AnalyzeRequest struct {
	Text string `json:"text"`
}

type AnalyzeResponse struct {
	Status         string    `json:"status"`
	WordCount      int       `json:"word_count"`
	CharacterCount int       `json:"character_count"`
	LineCount      int       `json:"line_count"`
	ByteSize       int       `json:"byte_size"`
	Service        string    `json:"service"`
	ProcessedAt    time.Time `json:"processed_at"`
}

type AnalyzeHandler struct{}

func NewAnalyzeHandler() *AnalyzeHandler {
	return &AnalyzeHandler{}
}

func (h *AnalyzeHandler) HandleAnalyze(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		_ = json.NewEncoder(w).Encode(map[string]string{
			"error": "method not allowed",
		})
		return
	}

	var req AnalyzeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		_ = json.NewEncoder(w).Encode(map[string]string{
			"error": "invalid JSON body",
		})
		return
	}

	text := req.Text
	words := strings.Fields(text)
	wordCount := len(words)
	characterCount := len([]rune(text))
	byteSize := len(text)

	lineCount := 0
	if text != "" {
		lineCount = strings.Count(text, "\n") + 1
	}

	resp := AnalyzeResponse{
		Status:         "success",
		WordCount:      wordCount,
		CharacterCount: characterCount,
		LineCount:      lineCount,
		ByteSize:       byteSize,
		Service:        "Go High-Performance Microservice",
		ProcessedAt:    time.Now().UTC(),
	}

	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}
