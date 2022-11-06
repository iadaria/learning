package main

import (
	"fmt"
)

func main() {

	intCh := make(chan int)

	go factorialInfinite(7, intCh)

	for num := range intCh {
		fmt.Println(num)
	}

	for {
		num, opened := <-intCh
		if !opened {
			break
		}
		fmt.Println(num)
	}
}

func factorialInfinite(n int, ch chan int) {
	defer close(ch)
	result := 1
	for i := 1; i <= n; i++ {
		result *= i
		ch <- result
	}
}

func factorialWithChans(n int, ch chan struct{}, results map[int]int) {
	defer close(ch)
	result := 1
	for i := 1; i <= n; i++ {
		result *= i
		results[i] = result
	}
}

func showChans() {
	intCh := make(chan int, 3)
	intCh <- 10
	intCh <- 3
	close(intCh)
	for i := 0; i < cap(intCh); i++ {
		if val, opened := <-intCh; opened {
			fmt.Println(val)
		} else {
			fmt.Println("Channel closed!")
		}
	}
}

func createChan(n int) chan int {
	ch := make(chan int)

	go func() {
		ch <- n
	}()

	return ch
}

func factorialWithChan(n int, ch chan int) {
	result := 1
	for i := 1; i <= n; i++ {
		result *= i
	}

	ch <- result
}
