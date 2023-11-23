package main

import (
	"bufio"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io"
	"io/ioutil"
	"net"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"
)

type Record struct {
	Name string
	Surname string
	Tel []Telephone
}

type Telephone struct {
	Mobile bool
	Number string
}

// ************** XML **************

func modXML() {
	type Address struct {
		City, Country string
	}

	type Employee struct {
		XMLName xml.Name `xml:"employee"`
		Id int `xml:"id,attr"`
		FirstName string `xml:"name>first"`
		LastName string `xml:"name>last"`
		Initials string `xml:"name>initials"`
		Height float32 `xml:"height,omitempty"`
		Address
		Comment string `xml:",comment"`
	}

	r := &Employee{Id: 7, FirstName: "Dahs", LastName: "Hz", Initials: "YAD"}
	r.Comment = "Technical Writer + DevOps"
	r.Address = Address{"SomeWhere 12", "12312, Greece"}

	output, err := xml.MarshalIndent(r, " ", " ")
	if err != nil {
		fmt.Println("Error:", err)
	}
	output = []byte(xml.Header + string(output))
	os.Stdout.Write(output)
	os.Stdout.Write([]byte("\n"))
}

// *********** read XML **************

func loadFromXML(filename string, key interface{}) error {
	in, err := os.Open(filename)
	if err != nil {
		return err
	}
	decodeXML := xml.NewDecoder(in)
	err = decodeXML.Decode(key)
	if err != nil {
		return err
	}
	in.Close()
	return nil
}

func readXML() {
	argument := os.Args
	if len(argument) == 1 {
		fmt.Println("Please privde a filename!")
		return
	}

	filename := argument[1]

	var myRecord Record
	err := loadFromXML(filename, &myRecord)
	if err == nil {
		fmt.Println("XML:", myRecord)
	} else {
		fmt.Println(err)
	}
}

// *********** write XML **************
func rwXML() {
	argument := os.Args
	if len(argument) == 1 {
		fmt.Println("Please privde a filename!")
		return
	}

	filename := argument[1]

	var myRecord Record
	err := loadFromJSON(filename, &myRecord)
	if err == nil {
		fmt.Println("JSON:", myRecord)
	} else {
		fmt.Println(err)
	}

	myRecord.Name = "Dimitris"

	xmlData, _ := xml.MarshalIndent(myRecord, "", "    ")
	xmlData = []byte(xml.Header + string(xmlData))
	fmt.Println("\nxmlData:", string(xmlData))

	data := &Record{}
	err = xml.Unmarshal(xmlData, data)
	if nil != err {
		fmt.Println("Unmarshalling from XML", err)
		return
	}

	result, err := json.Marshal(data)
	if nil != err {
		fmt.Println("Error marshalling to JSON", err)
		return
	}

	_ = json.Unmarshal([]byte(result), &myRecord)
	fmt.Println("\nJSON", myRecord)
}

// ************ JSON *************
func parsingJSON() {
	argument := os.Args
	if len(argument) == 1 {
		fmt.Println("Please privde a filename!")
		return
	}

	filename := argument[1]

	fileData, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println(err)
		return
	}
	var parsedData map[string]interface{}
	json.Unmarshal([]byte(fileData), &parsedData)

	for key, value := range parsedData {
		fmt.Println("key:", key, "value:", value)
	}
}

// *********** JSON **************

func readAndWriteMUJSON() {
	myRecord := Record{
		Name: "Dasha",
		Surname: "Iakimova",
		Tel: []Telephone{Telephone{Mobile: true, Number: "1234-5667"},
			Telephone{Mobile: true, Number: "1234-absc"},
			Telephone{Mobile: false, Number: "abcd-5667"},
		},
	}
	rec, err := json.Marshal(&myRecord)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(string(rec))

	var unRec Record
	err1 := json.Unmarshal(rec, &unRec)
	if err1 != nil {
		fmt.Println(err1)
		return
	}
	fmt.Println(unRec)
}

func loadFromJSON(filename string, key interface{}) error {
	in, err := os.Open(filename)
	if err != nil {
		return err
	}

	decodeJSON := json.NewDecoder(in)
	err = decodeJSON.Decode(key)
	if err != nil {
		return err
	}
	in.Close()
	return nil
}

func readJSON() {
	argument := os.Args
	if len(argument) == 1 {
		fmt.Println("Please privde a filename!")
		return
	}

	filename := argument[1]

	var myRecord Record
	err := loadFromJSON(filename, &myRecord)
	if err == nil {
		fmt.Println(myRecord)
	} else {
		fmt.Println(err)
	}
}

func saveToJSON(filename *os.File, key interface{}) {
	encodeJSON := json.NewEncoder(filename)
	err := encodeJSON.Encode(key)
	if err != nil {
		fmt.Println(err)
		return
	}
}

func makeJSON() {
	myRecord := Record{
		Name: "Dasha",
		Surname: "Iakimova",
		Tel: []Telephone{Telephone{Mobile: true, Number: "1234-5667"},
			Telephone{Mobile: true, Number: "1234-absc"},
			Telephone{Mobile: false, Number: "abcd-5667"},
		},
	}
	saveToJSON(os.Stdout, myRecord)
}


//*********************

type aStructure struct {
	person string
	height int
	weight int
}

type myElement struct {
	Name string
	Surname string
	Id string
}

var DATA = make(map[string]myElement)

func ADD(k string, n myElement) bool {
	if k == "" {
		return false
	}
	if LOOKUP(k) == nil {
		DATA[k] = n
		return true
	}
	return false
}

func LOOKUP(k string) *myElement {
	_, ok := DATA[k]
	if ok {
		n := DATA [k]
		return &n
	} else {
		return nil
	}
}

func DELETE(k string) bool {
	if LOOKUP(k) != nil {
		delete(DATA, k)
		return true
	}
	return false
}

func CHANGE(k string, n myElement) bool {
	DATA[k] = n
	return true
}

func PRINT() {
	for k, d := range DATA {
		fmt.Printf("key: %s value: %v\n", k, d)
	}
}

func keyClient() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		text := scanner.Text()
		text = strings.TrimSpace(text)
		tokens := strings.Fields(text)

		switch len(tokens) {
		case 0:
			continue
		case 1:
			tokens = append(tokens, "")
			tokens = append(tokens, "")
			tokens = append(tokens, "")
			tokens = append(tokens, "")
			fmt.Println("1", tokens)
		case 2:
			tokens = append(tokens, "")
			tokens = append(tokens, "")
			tokens = append(tokens, "")
			fmt.Println("2", tokens)
		case 3:
			tokens = append(tokens, "")
			tokens = append(tokens, "")
			fmt.Println("3", tokens)
		case 4:
			tokens = append(tokens, "")
			fmt.Println("4", tokens)
		}

		switch tokens[0] {
		case "PRINT":
			PRINT()
		case "STOP":
			return
		case "DELETE":
			if !DELETE(tokens[1]) {
				fmt.Println("Delete operation failed!")
			}
		case "ADD":
			n := myElement{tokens[2], tokens[3], tokens[4]}
			if !ADD(tokens[1], n) {
				fmt.Println("Add operation failed!")
			}
		case "CHANGE":
			n := myElement{tokens[2], tokens[3], tokens[4]}
			if !CHANGE(tokens[1], n) {
				fmt.Println("Update operation failed!")
			}
		default:
			fmt.Println("Unknown command - please try again!")
		}
	}
}

func runes() {
	fmt.Println("A string is a collection of runes:", []byte("Mihalis"))
	aString := []byte("Mihalis")
	for x, y := range aString {
		fmt.Println(x, y)
		fmt.Printf("Char: %c\n", aString[x])
	}
	fmt.Printf("%s\n", aString)
}

func findIP(input string) string {
	partIP := "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"
	grammar := partIP + "\\." + partIP + "\\." + partIP + "\\." + partIP
	matchMe := regexp.MustCompile(grammar)
	return matchMe.FindString(input)
}

func ch04_findIP() {
	arguments := os.Args
	if len(arguments) < 2 {
		fmt.Printf("usage: %s logFile\n", filepath.Base(arguments[0]))
		os.Exit(1)
	}

	for _, filename := range arguments[1:] {
		f, err := os.Open(filename)
		if err != nil {
			fmt.Printf("error opening file %s\n", err)
			os.Exit(-1)
		}
		defer f.Close()
		r := bufio.NewReader(f)
		for {
			line, err := r.ReadString('\n')
			if err == io.EOF {
				break
			} else if err != nil {
				fmt.Printf("error reading file %s", err)
			}
			
			ip := findIP(line)
			trial := net.ParseIP(ip)
			if trial.To4() == nil {
				continue
			}
			fmt.Println(ip)
		}
	}
	
}

func ch04_changeDT() {
	arguments := os.Args
	if len(arguments) == 1 {
		fmt.Printf("Please provide one text file to process!")
		return
	}

	filename := arguments[1]
	f, err := os.Open(filename)
	if err != nil {
		fmt.Printf("error opening file %s", err)
		return
	}
	defer f.Close()

	notAMatch := 0
	r := bufio.NewReader(f)
	for {
		line, err := r.ReadString('\n')
		if err == io.EOF {
			break
		} else if err != nil {
			fmt.Printf("error reading file %s", err)
		}
		r1 := regexp.MustCompile(`.*\[(\d\d/\w+\d\d\d\d:\d\d:\d\d:\d\d)\].*`)
		if r1.MatchString(line) {
			match := r1.FindStringSubmatch(line)
			d1, err := time.Parse("02/Jan/2006:15:04:05 -0700", match[1])
			if err == nil {
				newFormat := d1.Format(time.Stamp)
				fmt.Print(strings.Replace(line, match[1], newFormat, 1))
			} else {
				notAMatch++
			}
			continue
		}
	}
}

func ch04_ex1() {
	arguments := os.Args
	if len(arguments) < 2 {
		fmt.Printf("usage: selectColumn column <file> [<file2> [...<fileN>]]\n")
		return
	}
	
	temp, err := strconv.Atoi(arguments[1])
	if err != nil {
		fmt.Println("Column value is not an integer: ", temp)
		return
	}

	column := temp
	if column < 0 {
		fmt.Println("Invalid Column number!")
		os.Exit(1)
	}

	for _, filename := range arguments[2:] {
		fmt.Println("\t\t", filename)
		f, err := os.Open(filename)
		if err != nil {
			fmt.Printf("error opening file %s\n", err)
			continue
		}
		defer f.Close()

		r := bufio.NewReader(f)
		for {
			line, err := r.ReadString('\n')
			if err == io.EOF {
				break
			} else if err != nil {
				fmt.Printf("error reading file %s", err)
			}
			data := strings.Fields(line)
			if len(data) >= column {
				fmt.Println(((data[column-1])))
			}
		}
	}
}