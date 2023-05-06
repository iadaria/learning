package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
)

func exercise1_1() {
	arguments := os.Args
	length := len(arguments)

	if length == 1 {
		fmt.Println("Please give or more floats.")
		os.Exit(1)
	}

	var err error = errors.New("An error")
	k := 1
	var n int64
	
	for err != nil {
		if k >= length {
			fmt.Println("None of the argument is a float!")
			return
		}
		n, err = strconv.ParseInt(arguments[k], 16, 64)
		fmt.Println("At least one:", "value=", n, ", index=", k, "error is '", err)
		k++
	}
	
	count := 1
	
	for i := 2; i < length; i++ {
		if "END" == arguments[i] {
			break
		}

		n, err := strconv.ParseInt(arguments[i], 10, 64)
		fmt.Println("Counting:", "value=", n, ", index=",i, "error is '", err)
		if err == nil {
			count += 1
		}
	}
	fmt.Println("Count of integer numbers equals:", count)
}

func exercise1_0() {

	arguments := os.Args
	length := len(arguments)

	if length == 1 {
		fmt.Println("Please give or more floats.")
		os.Exit(1)
	}

	var err error = errors.New("An error")
	k := 1
	var n, sum, average float64
	
	for err != nil {
		if k >= length {
			fmt.Println("None of the argument is a float!")
			return
		}
		n, err = strconv.ParseFloat(arguments[k], 64)
		fmt.Println("n=", n, ", k=",k, "error is '", err)
		k++
	}

	sum = n
	count := 1

	for i := 2; i < length; i++ {
		n, err := strconv.ParseFloat(arguments[i],64)
		if err == nil {
			count += 1
			sum += n
		}
	}

	average = sum / float64(count)

	fmt.Println("Sum:", sum)
	fmt.Println("Average:", average)
}