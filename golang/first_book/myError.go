package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
)

func myError() {

	arguments := os.Args
	fmt.Println("len of arguments", len(arguments))
	var err error = errors.New("An error")
	k := 1
	var n float64

	for err != nil {
		if k >= len(arguments) {
			fmt.Println("None of the arguments is a float!")
			return
		}
		n, err = strconv.ParseFloat(arguments[k], 64)
		fmt.Println("n=", n, ", k=",k, "error is '", err)
		k++
	}

	min, max := n, n

	
	for i := 2; i < len(arguments); i++ {
		n, err := strconv.ParseFloat(arguments[i], 64)
		if err == nil {
			if n < min {
				min = n
			}
			if n > max {
				max = n
			}
		}
	}
	fmt.Println("Min:", min, ", Max:", max)
}