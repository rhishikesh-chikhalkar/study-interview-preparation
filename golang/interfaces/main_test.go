package main

import (
	"math"
	"testing"
)

func TestCircleArea(t *testing.T) {
	tests := []struct {
		name     string
		radius   float64
		expected float64
	}{
		{"Radius 0", 0, 0},
		{"Radius 1", 1, math.Pi},
		{"Radius 5", 5, 25 * math.Pi},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			c := Circle{Radius: tt.radius}
			actual := c.Area()
			if math.Abs(actual-tt.expected) > 1e-9 {
				t.Errorf("expected %f, got %f", tt.expected, actual)
			}
		})
	}
}

func TestRectangleArea(t *testing.T) {
	tests := []struct {
		name     string
		width    float64
		height   float64
		expected float64
	}{
		{"Zero dimensions", 0, 0, 0},
		{"Normal rectangle", 5, 10, 50},
		{"Square", 4, 4, 16},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			r := Rectangle{Width: tt.width, Height: tt.height}
			actual := r.Area()
			if actual != tt.expected {
				t.Errorf("expected %f, got %f", tt.expected, actual)
			}
		})
	}
}

func TestPolymorphism(t *testing.T) {
	// Verify that Circle and Rectangle actually implement the Shape interface
	var s Shape

	s = Circle{Radius: 2}
	expectedCircleArea := 4 * math.Pi
	if math.Abs(s.Area()-expectedCircleArea) > 1e-9 {
		t.Errorf("Circle polymorphism failed: expected %f, got %f", expectedCircleArea, s.Area())
	}

	s = Rectangle{Width: 3, Height: 4}
	expectedRectArea := 12.0
	if s.Area() != expectedRectArea {
		t.Errorf("Rectangle polymorphism failed: expected %f, got %f", expectedRectArea, s.Area())
	}
}
