package main

import (
	"fmt"

	"github.com/iadaria/celeritas"
)

func main() {
	result := celeritas.TestFunc(1, 1)
	fmt.Println(result)

	result = celeritas.TestFunc2(2, 1)
	fmt.Println(result)

	result = celeritas.TestFunc0(1, 2)
	fmt.Println(result)
}
