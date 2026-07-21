package main

import (
	"fmt"
	"math"
)

// Shape defines the contract for geometric shapes that have an area.
type Shape interface {
	Area() float64
}

// Circle represents a circle with a given radius.
type Circle struct {
	Radius float64
}

// Area calculates and returns the area of the circle: π * r^2.
func (c Circle) Area() float64 {
	return math.Pi * c.Radius * c.Radius
}

// Rectangle represents a rectangle with a given width and height.
type Rectangle struct {
	Width  float64
	Height float64
}

// Area calculates and returns the area of the rectangle: width * height.
func (r Rectangle) Area() float64 {
	return r.Width * r.Height
}

// PrintShapeInfo demonstrates interface polymorphism.
// It accepts any type that implements the Shape interface.
func PrintShapeInfo(s Shape) {
	fmt.Printf("Shape Type: %T, Area: %.4f\n", s, s.Area())
}

func main() {
	fmt.Println("--- Learning Go Interfaces ---")

	// Create instances of Circle and Rectangle
	c := Circle{Radius: 5}
	r := Rectangle{Width: 10, Height: 5}

	// Use polymorphism via function argument
	PrintShapeInfo(c)
	PrintShapeInfo(r)

	// Declare a slice of Shapes
	shapes := []Shape{
		Circle{Radius: 3},
		Rectangle{Width: 4, Height: 6},
		Circle{Radius: 10},
	}

	fmt.Println("\nIterating through a slice of Shape interfaces:")
	for _, shape := range shapes {
		PrintShapeInfo(shape)
	}
}
