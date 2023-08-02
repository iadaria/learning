package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"time"
)

type DayOfWeek int
type Power4 int64

// Напишите генератор константы iota для дней недели
func ex_1() {
	const (
		Mondey DayOfWeek = iota + 1
		Tuesday
		Wednesday
		Thursday
		Friday
		Saturday
		Sunday
	)

	fmt.Println(Mondey, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)
}

// Напишите программу Go,  которая бы преобразовывала заданный массив в хеш-таблицу
func ex_2() {
	anArray := [4]int{1, 2, 4, -4}
	aMap := make(map[int]int)
	for key, value := range anArray {
		aMap[key] = value
	}
	fmt.Println(aMap)
}

// Сможете ли вы написать генератор контстанты iota для степеней числа четыре?
func ex_3() {
 const (
	p4_1 Power4 = 1 << iota << iota
	p4_2
	p4_3
	p4_4
 )

 fmt.Println(p4_1, p4_2, p4_3, p4_4)
 fmt.Println(strconv.FormatInt(int64(p4_1), 2))
 fmt.Println(strconv.FormatInt(int64(p4_2), 2))
 fmt.Println(strconv.FormatInt(int64(p4_3), 2))
 fmt.Println(strconv.FormatInt(int64(p4_4), 2))
}

// Напишите собственную версию parseDate.go
func ex_4() {
 var myDate string
 if len(os.Args) != 2 {
	//fmt.Println(os.Args[0])
	fmt.Printf("usage: %s string\n", filepath.Base(os.Args[0]))
	return
 }
 myDate = os.Args[1]
 d, err := time.Parse("02 01 2006", myDate)
 if err == nil {
	fmt.Println("Full:", d)
	fmt.Println("Time:", d.Day(), d.Month(), d.Year())
 } else {
	fmt.Println(err)
 }
}

// Напишите собственную версию parseTime.go. Не забудьте протестировать вышу программу
func ex_5() {
	var myTime string
	if len(os.Args) != 2 {
		fmt.Printf("usage: % string", filepath.Base(os.Args[0]))
		os.Exit(1)
	}
	myTime = os.Args[1]

	d, err := time.Parse("15:04:05", myTime)
	if err == nil {
		fmt.Println("Full:",d)
		fmt.Println("Time:", d.Hour(), d.Minute())
	} else {
		fmt.Println(err)
	}
}

//Сможете ли вы создать версию timeDate.go, которая бы обрабатывала два формата даты и времени?
func ex_6() {
	logs := []string{"127.0.0.1 - - [16/Nov/2017:10:49:46 +0200] 325504",
		"127.0.0.1 - - [16/Nov/2017:10:16:41 +0200] \"GET /CVEN HTTP/1.1\" 200 12531 \"-\" \"Mozilla/5.0 AppleWebKit/537.36",
		"127.0.0.1 200 9412 - - [12/Nov/2017:06:26:05 +0200] \"GET \"http://www.mtsoukalos.eu/taxonomy/term/47\" 1507",
		"[12/Nov/2017:16:27:21 +0300]",
		"[12/Nov/2017:20:88:21 +0200]",
		"[12/Nov/2017:20:21 +0200]",
	}
	for _, logEntry := range logs {
		r := regexp.MustCompile(`.*\[(\d\d/\w+/\d\d\d\d:\d\d:\d\d.*)\].*`)
		if r.MatchString(logEntry) {
			match := r.FindStringSubmatch(logEntry)
			dt, err := time.Parse("02/Jan/2006:15:04:05 -0700", match[1])
			if err == nil {
				newFormat := dt.Format(time.RFC850)
				fmt.Println(newFormat)
			} else {
				fmt.Println("Not a valid date time format!")
			}
		} else {
			fmt.Println("Not a match!")
		}
	}
}

func slice_1() {
	// aSliceLiteral := []int{1, 2, 3, 4, 5}
	integer := make([]int, 20)
	integer = append(integer, 123)
	fmt.Println(integer)
	for i := 0; i < len(integer); i++ {
		fmt.Println(integer[i])
	}
}

func slice_2() {
	bytes := make([]byte, 5)
	fmt.Println(bytes)
} 
