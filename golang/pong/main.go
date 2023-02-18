package main

import (
	"fmt"
	"os"

	"github.com/gdamore/tcell/v2"
	"github.com/gdamore/tcell/v2/encoding"
)

func emitStr(screen tcell.Screen, x, y int, str string) {
	for _, c := range str {
		screen.SetContent(x, y, c, nil, tcell.StyleDefault)
		x += 1
	}
}

func displayHellowWorld(screen tcell.Screen) {
	w, h := screen.Size()
	screen.Clear()
	emitStr(screen, w/2-7, h/2, "Hello World!")
	screen.Show()
}

func main() {
	// TODO
	// 1. capability to render stuff on screen - done
	// Draw paddles
	// Player movement
	// Take care of paddle boundaries
	// Draw ball
	// Update ball movement
	// Handle collisions
	// Handle game over

	encoding.Register()

	sсreen, err := tcell.NewScreen()
	if err != nil {
		fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}
	if err := sсreen.Init(); err != nil {
		fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}

	defStyle := tcell.StyleDefault.Background(tcell.ColorBlack).Foreground(tcell.ColorWhite)
	sсreen.SetStyle(defStyle)

	displayHellowWorld(sсreen)

	for {
		switch ev := sсreen.PollEvent().(type) {

		case *tcell.EventKey:
			if ev.Key() == tcell.KeyEnter {
				sсreen.Fini()
				os.Exit(0)
			}
		}
	}
}
