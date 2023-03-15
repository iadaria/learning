package computation

import "fmt"

func Factorial(n int) {
	if n < 1 {
		fmt.Println("Invalid input number")
		return
	}
	var result = 1
	for i := 1; i <= n; i++ {
		result *= i
	}
	fmt.Println(n, "-", result)
}
