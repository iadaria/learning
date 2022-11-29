package main

import "fmt"

type node struct {
	value int
	next  *node
}

func derivedType() {
	first := node{value: 4}
	second := node{value: 5}
	third := node{value: 6}

	first.next = &second
	second.next = &third

	var current *node = &first
	for current != nil {
		fmt.Println(current.value)
		current = current.next
	}
}

func printNodeValue(n *node) {
	fmt.Println(n.value)
	if n.next != nil {
		printNodeValue(n.next)
	}
}
