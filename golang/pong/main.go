// TODO The auto rebuild 'gomon'
//Interesting https://levelup.gitconnected.com/how-to-watch-for-file-change-in-golang-4d1eaa3d2964

// TODO
// DONE - 1. capability to render stuff on screen - done
// DONE - 2. Draw paddles
// DONE - 3 User input
// DONE - 4 Player movement
// Take care of paddle boundaries
// Draw ball
// Update ball movement
// Handle collisions
// Handle game over

package main

import (
	"fmt"
	"os"
	"time"

	"github.com/gdamore/tcell/v2"
	"github.com/gdamore/tcell/v2/encoding"
)

const paddleSymbol = 0x2588
const paddleHeight = 8
const paddleWidth = 1

type Paddle struct {
	row, col, width, height int
}

var screen tcell.Screen
var player1 *Paddle
var player2 *Paddle
var debugLog string

func main() {
	InitScreen()
	InitGameStage()
	DrawState()
	inputChan := InitUserInput()

	for {
		DrawState()
		time.Sleep(50 * time.Millisecond)

		key := ReadInput(inputChan)
		HandleUserInput(key)
	}
}

func InitScreen() {
	encoding.Register()

	var err error
	screen, err = tcell.NewScreen()

	if err != nil {
		fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}
	if err := screen.Init(); err != nil {
		fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}

	defStyle := tcell.StyleDefault.Background(tcell.ColorDarkOliveGreen.TrueColor()).Foreground(tcell.ColorWhite)
	screen.SetStyle(defStyle)
}

func InitGameStage() {
	width, height := screen.Size()
	paddleStart := height/2 - paddleHeight/2

	player1 = &Paddle{
		row: paddleStart, col: 0, width: paddleWidth, height: paddleHeight,
	}
	player2 = &Paddle{
		row: paddleStart, col: width - 1, width: paddleWidth, height: paddleHeight,
	}
}

func InitUserInput() chan string {
	inputChan := make(chan string)
	go func() {
		for {
			switch ev := screen.PollEvent().(type) {
			case *tcell.EventKey:
				// TODO:
				//debugLog = ev.Name()
				inputChan <- ev.Name()
			}
		}
	}()

	return inputChan
}

func ReadInput(inputChan chan string) string {
	var key string
	select {
	case key = <-inputChan:
	default:
		key = ""
	}

	return key
}

func DrawState() {
	screen.Clear()
	PrintString(0, 0, debugLog)
	Print(player1.row, player1.col, player1.width, player1.height, paddleSymbol)
	Print(player2.row, player2.col, player2.width, player2.height, paddleSymbol)
	screen.Show()
}

func PrintString(col, row int, str string) {
	for _, char := range str {
		screen.SetContent(col, row, char, nil, tcell.StyleDefault)
		col += 1
	}
}
func Print(startRow, startCol, width, height int, ch rune) {
	defStyle := tcell.StyleDefault.Background(tcell.ColorLightGoldenrodYellow).Foreground(tcell.ColorWhite)
	for row := 0; row < height; row++ {
		for column := 0; column < width; column++ {
			screen.SetContent(startCol+column, startRow+row, ch, nil, defStyle)
		}
	}
}

func HandleUserInput(key string) {
	_, screenHeight := screen.Size()

	if key == "Rune[q]" {
		screen.Fini()
		os.Exit(0)
	} else if key == "Rune[w]" && player1.row > 0 {
		player1.row--
	} else if key == "Rune[s]" && player1.row+player1.height < screenHeight {
		player1.row++
	} else if key == "Up" && player2.row > 0 {
		player2.row--
	} else if key == "Down" && player2.row+player2.height < screenHeight {
		player2.row++
	}
}
