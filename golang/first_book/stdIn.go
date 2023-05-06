package main

import (
	"bufio"
	"fmt"
	"os"
)

func stdIn() {
	var f *os.File
	f = os.Stdin
	defer f.Close()
	
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fmt.Println(">", scanner.Text())
	}
}