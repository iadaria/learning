// TODO
// DONE - 1. capability to render stuff on screen - done
// DONE - 2. Draw paddles
// Player movement
// Take care of paddle boundaries
// Draw ball
// Update ball movement
// Handle collisions
// Handle game over

package main

import (
	"fmt"
	"os"

	"github.com/gdamore/tcell/v2"
	"github.com/gdamore/tcell/v2/encoding"
)

const paddleSymbol = 0x2588
const paddleHeight = 4
const paddleWidth = 1

type Paddle struct {
	row, col, width, height int
}

var screen tcell.Screen
var player1 *Paddle
var player2 *Paddle

func printString(col, row int, str string) {
	for _, char := range str {
		screen.SetContent(col, row, char, nil, tcell.StyleDefault)
		col += 1
	}
}
func print(startRow, startCol, width, height int, ch rune) {
	defStyle := tcell.StyleDefault.Background(tcell.Color100).Foreground(tcell.ColorWhite)
	for row := 0; row < height; row++ {
		for column := 0; column < width; column++ {
			screen.SetContent(startCol+column, startRow+row, ch, nil, defStyle)
		}
	}
}

func drawState() {
	screen.Clear()
	print(player1.row, player1.col, player1.width, player1.height, paddleSymbol)
	print(player2.row, player2.col, player2.width, player2.height, paddleSymbol)
	screen.Show()
}

func main() {
	initScreen()

	initGameStage()

	drawState()

	for {
		switch ev := screen.PollEvent().(type) {

		case *tcell.EventKey:
			if ev.Key() == tcell.KeyEnter {
				screen.Fini()
				os.Exit(0)
			}
		}
	}

}

func initScreen() {
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

	defStyle := tcell.StyleDefault.Background(tcell.ColorBlack).Foreground(tcell.ColorWhite)
	screen.SetStyle(defStyle)
}

func initGameStage() {
	width, height := screen.Size()
	paddleStart := height/2 - paddleHeight/2

	player1 = &Paddle{
		row: paddleStart, col: 0, width: paddleWidth, height: paddleHeight,
	}
	player2 = &Paddle{
		row: paddleStart, col: width - 1, width: paddleWidth, height: paddleHeight,
	}
}
