package main

import "fmt"

func addTwoNumbers(a int, b int) int {
	return a + b
}

func main() {
	for i := 0; i < 10; i++ {
		fmt.Println(addTwoNumbers(i, i))
	}
}
