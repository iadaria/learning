package main

import "fmt"

func slice_1() {
	// aSliceLiteral := []int{1, 2, 3, 4, 5}
	integer := make([]int, 20)
	integer = append(integer, 123)
	for i := 0; i < len(integer); i++ {
		fmt.Println(integer[i])
	}
}