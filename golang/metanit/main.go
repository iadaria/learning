package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	polymorphismMain()
}

// WaitGroup
func waitGroup() {
	var wg sync.WaitGroup
	wg.Add(2)
	workSecond := func(id int) {
		defer wg.Done()
		fmt.Printf("Goroutine %d started executing \n", id)
		time.Sleep(2 * time.Second)
		fmt.Printf("Goroutine %d finished executing \n", id)
	}
	go workSecond(1)
	go workSecond(2)

	wg.Wait()
	fmt.Printf("Goroutines finished executing")
}

// Mutexe
var counter int = 0

func mutex() {

	ch := make(chan bool)
	var mutex sync.Mutex
	for i := 1; i < 5; i++ {
		go work(i, ch, &mutex)
	}

	// waiting for finishing of all goroutine
	for i := 1; i < 5; i++ {
		<-ch
	}

	fmt.Println("The End")
}

func work(number int, ch chan bool, mutex *sync.Mutex) {
	mutex.Lock()
	counter = 0
	for k := 1; k <= 5; k++ {
		counter++
		fmt.Println("Goroutine", number, "-", counter)
	}
	mutex.Unlock()
	ch <- true
}

func passingOfDataStreams() {
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
