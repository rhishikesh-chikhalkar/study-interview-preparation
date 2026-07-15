package main

import "fmt"

func greeting(name string) string {
	message := fmt.Sprintf("Hi %v, Welcome!", name)
	return message
}

func main() {
	fmt.Println(greeting("Rhishikesh"))
}
