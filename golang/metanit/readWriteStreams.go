package main

import (
	"fmt"
	"io"
)

// io.Writer

type phoneWriter struct{}

func (p phoneWriter) Write(bs []byte) (int, error) {
	if len(bs) == 0 {
		return 0, nil
	}

	for i := 0; i < len(bs); i++ {
		if bs[i] >= '0' && bs[i] <= '9' {
			fmt.Print(string(bs[i]))
		}
	}
	fmt.Println()
	return len(bs), nil
}

func writePhones() {
	bytes1 := []byte("+1(234)5679010")

	writer := phoneWriter{}
	writer.Write(bytes1)
}

// io.Reader

type phoneReader string

func (ph phoneReader) Read(p []byte) (int, error) {
	count := 0
	for i := 0; i < len(ph); i++ {
		if ph[i] >= '0' && ph[i] <= '9' {
			p[count] = ph[i]
			count++
		}
	}
	return count, io.EOF
}

func readPhones() {
	phone1 := phoneReader("+1(234)567 9010")
	phone2 := phoneReader("+2-345-678-12-35")

	buffer := make([]byte, len(phone1))
	phone1.Read(buffer)
	fmt.Println(string(buffer))

	buffer = make([]byte, len(phone2))
	phone2.Read(buffer)
	fmt.Println(string(buffer))
}
