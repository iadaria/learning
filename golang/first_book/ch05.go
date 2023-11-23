package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

//********** Linked list - LL *************

type LLNode struct {
	Value int
	Next *LLNode
}

var root = new(LLNode)

func addLLNode(t *LLNode, v int) int {
	if root == nil {
		t = &LLNode {v, nil}
		root = t
		return 0
	}

	if v == t.Value {
		fmt.Println("Node already exists:", v)
		return -1
	}

	if t.Next == nil {
		t.Next = &LLNode{v, nil}
		return -2
	}

	return addLLNode(t.Next, v)
}

func traverseLL(t *LLNode) {
	if t == nil {
		fmt.Println("-> Empty list!")
		return
	}

	for t != nil {
		fmt.Printf("%d ->", t.Value)
		t = t.Next
	}
	fmt.Println()
}

func lookupLLNode(t *LLNode, v int) bool {
	if root == nil {
		t = &LLNode{v, nil}
		root = t
		return false
	}

	if v == t.Value {
		return true
	}

	if t.Next == nil {
		return false
	}

	return lookupLLNode(t.Next, v)
}

func deleteLLNode(t *LLNode, v int) bool {
	if root == nil {
		return false
	}

	return lookupLLNode(t.Next, v)
}

func sizeLL(t *LLNode) int {
	if t == nil {
		fmt.Println("-> Empty list!")
		return 0
	}

	i :=0
	for t != nil {
		i++
		t = t.Next
	}
	return i
}

func clientLL() {
	fmt.Println(root)
	root = nil
	traverseLL(root)
	addLLNode(root, 1)
	addLLNode(root, -1)
	traverseLL(root)
	addLLNode(root, 10)
	addLLNode(root, 5)
	addLLNode(root, 45)
	addLLNode(root, 5)
	addLLNode(root, 6)
	addLLNode(root, 100)
	traverseLL(root)

	if lookupLLNode(root, -100) {
		fmt.Println("Node exists!")
	} else {
		fmt.Println("Node does not exist!")
	}

	deleteLLNode(root, 45)
}

//********** Hash-table *************

// Количество блоков
const SIZE = 15

type HTNode struct {
	Value int
	Next *HTNode
}

type HashTable struct {
	Table map[int]*HTNode
	Size int
}

func hashFunction(i, size int) int {
	return (i % size)
}

func insertIntoHashTable(hash *HashTable, value int) int {
	index := hashFunction(value, hash.Size)
	element := HTNode{Value: value, Next: hash.Table[index]}
	hash.Table[index] = &element
	return index
}

func traverseHashTable(hash *HashTable) {
	for k := range hash.Table {
		if hash.Table[k] != nil {
			t := hash.Table[k]
			for t != nil {
				fmt.Printf("%d -> ", t.Value)
				t = t.Next
			}
			fmt.Println()
		}
	}
}

func lookupHashTable(hash *HashTable, value int) bool {
	index := hashFunction(value, hash.Size)
	if hash.Table[index] != nil {
		t := hash.Table[index]
		for t != nil {
			if t.Value == value {
				return true
			}
			t = t.Next
		}
	}
	return false
}

func clientHashTable() {
	table := make(map[int]*HTNode, SIZE)
	hash := &HashTable{Table: table, Size: SIZE}
	fmt.Println("Number of spaces:", hash.Size)
	for i := 0; i < 120; i++ {
		insertIntoHashTable(hash, i)
	}
	traverseHashTable(hash)

	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("-> ")
		text, _ := reader.ReadString('\n')
		text = strings.Replace(text, "\n", "", -1)
		digit, err := strconv.Atoi(text)
		if err != nil {
			fmt.Println("Enter the digit from 0 to 120")
			continue
		}
		found := lookupHashTable(hash, digit)
		if found {
			fmt.Printf("%d belongs to the hash table", digit)
			} else {
				fmt.Printf("%d doesnt belong to the hash table", digit)
		}
		fmt.Println()
	}
}

//********** Tree *************

type Tree struct {
	Left *Tree
	Value int
	Right *Tree
}

func traverse(t *Tree) {
	if t == nil {
		return
	}
	traverse(t.Left)
	fmt.Print(t.Value, " ")
	traverse(t.Right)
}

func create(n int) *Tree {
	var t *Tree
	rand.Seed(time.Now().Unix())
	for i := 0; i < 2*n; i ++ {
		temp := rand.Intn(n * 2)
		t = insert(t, temp)
	}
	return t
}

func insert(t *Tree, v int) *Tree {
	if t == nil {
		return &Tree{nil, v, nil}
	}
	if v == t.Value {
		return t
	}
	if v < t.Value {
		t.Left = insert(t.Left, v)
		return t
	}
	t.Right = insert(t.Right, v)
	return t
}

func binaryTreeClient() {
	tree := create(10)
	fmt.Println("The value of the root of tree is", tree.Value)
	traverse(tree)
	fmt.Println()
	tree = insert(tree, -10)
	tree = insert(tree, -2)
	tree = insert(tree, 14)
	traverse(tree)
	fmt.Println()
	fmt.Println("The value of the root of tree is", tree.Value)
}