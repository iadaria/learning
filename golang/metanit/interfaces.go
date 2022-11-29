package main

import "fmt"

//

type Vehicle interface {
	move()
}

type Car struct{}

type Aircraft struct{}

func (c Car) move() {
	fmt.Println("The car is driving")
}

func (a Aircraft) move() {
	fmt.Println("The plane is flying")
}

func interfaceMain() {
	var tesla Vehicle = Car{}
	var boing Vehicle = Aircraft{}
	tesla.move()
	boing.move()
}

type Stream interface {
	read() string
	write(string)
	close()
}

func writeToStream(stream Stream, text string) {
	stream.write(text)
}

func closeStream(stream Stream) {
	stream.close()
}

type File struct {
	text string
}

type Folder struct{}

func (f *File) read() string {
	return f.text
}

func (f *File) write(message string) {
	f.text = message
	fmt.Println("Writing a row into the file ")
}

func (f *File) close() {
	fmt.Println(("File is closed."))
}

func (f *Folder) close() {
	fmt.Println("Folder is closed.")
}

func streamMain() {
	myFile := &File{}
	myFolder := &Folder{}

	writeToStream(myFile, "hello world")
	closeStream(myFile)
	myFolder.close()
}

// Multiple interfaces

type Reader interface {
	read() string
}

type Writer interface {
	write(string)
}

type ReaderWriter interface {
	Reader
	Writer
}

func writeIntoStream(writer ReaderWriter, text string) {
	writer.write(text)
}

func readFromStream(reader ReaderWriter) {
	reader.read()
}

func readerWriterMain() {
	myFile := &File{}
	writeIntoStream(myFile, "hello world")
	readFromStream(myFile)
	writeToStream(myFile, "loly")
	readFromStream(myFile)
}
