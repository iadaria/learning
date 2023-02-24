// TODO The auto rebuild 'gomon'
//Interesting https://levelup.gitconnected.com/how-to-watch-for-file-change-in-golang-4d1eaa3d2964

// TODO
// * DONE - 1. capability to render stuff on screen - done
// * DONE - 2. Draw paddles
// * DONE - 3 User input
// * DONE - 4 Player movement
// * DONE - 5 Take care of paddle boundaries
// * DONE - 6 Draw ball
// * DONE - 7 Update ball movement
// * DONE - 8 Handle ball to wall collision
// * DONE - 9 Handle ball to paddle collision
// ? 10 Handle game over
// ? 10 Handle game over
// ! Exit
// @param myParam The

package main

import (
	"fmt"
	"os"
	"time"

	"github.com/gdamore/tcell/v2"
	"github.com/gdamore/tcell/v2/encoding"
)

const PaddleSymbol = 0x2588
const BallSymbol = 0x25CF
const paddleHeight = 8
const paddleWidth = 1
const InitialBallVelocityRow = 1
const InitialBallVelocityCol = 2
const timeout = 100

type GameObject struct {
	row, col, width, height int
	velRow, velCol          int
	symbol                  rune
}

var screen tcell.Screen
var player1 *GameObject
var player2 *GameObject
var ball *GameObject
var debugLog string
var isGamePaused = false

var gameObjects []*GameObject

func main() {
	InitScreen()
	InitGameStage()
	DrawState()
	inputChan := InitUserInput()

	for {
		HandleUserInput(ReadInput(inputChan))
		UpdateState()
		DrawState()

		time.Sleep(timeout * time.Millisecond)
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

	player1 = &GameObject{
		row: paddleStart, col: 0, width: paddleWidth, height: paddleHeight,
		velRow: 0, velCol: 0,
		symbol: PaddleSymbol,
	}

	player2 = &GameObject{
		row: paddleStart, col: width - 1, width: paddleWidth, height: paddleHeight,
		velRow: 0, velCol: 0,
		symbol: PaddleSymbol,
	}

	ball = &GameObject{
		row: height / 2, col: width / 2, width: 1, height: 1,
		velRow: InitialBallVelocityRow, velCol: InitialBallVelocityCol,
		symbol: BallSymbol,
	}

	gameObjects = []*GameObject{
		player1, player2, ball,
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

// some anymation: color
func UpdateState() {
	if isGamePaused {
		return
	}
	for i := range gameObjects {
		gameObjects[i].row += gameObjects[i].velRow
		gameObjects[i].col += gameObjects[i].velCol
	}

	debugLog = fmt.Sprintf("ball: row=%d, col=%d\npaddle 1: row=%d, col=%d\npaddle 2:row=%d, col=%d",
		ball.row, ball.col, player1.row, player1.col, player2.row, player2.col)
	if CollidesWithWall(ball) {
		ball.velRow = -ball.velRow
	}

	if CollidesWithPaddle(ball, player1) || CollidesWithPaddle(ball, player2) {
		ball.velCol = -ball.velCol
	}
}

func DrawState() {

	if isGamePaused {
		return
	}

	screen.Clear()
	PrintString(0, 0, debugLog)
	for _, obj := range gameObjects {
		Print(obj.row, obj.col, obj.width, obj.height, obj.symbol)
	}
	screen.Show()
}

func CollidesWithWall(obj *GameObject) bool {
	_, screenHeight := screen.Size()
	return obj.row+obj.velRow < 0 || obj.row+obj.velRow > screenHeight
}

func CollidesWithPaddle(ball *GameObject, paddle *GameObject) bool {
	var collidesOnColumn bool
	if ball.col < paddle.col {
		collidesOnColumn = ball.col+ball.velCol >= paddle.col
	} else {
		collidesOnColumn = ball.col+ball.velCol <= paddle.col
	}
	return collidesOnColumn &&
		ball.row >= paddle.row &&
		ball.row < paddle.row+paddle.height
}

func PrintString(col, row int, str string) {
	for _, char := range str {
		screen.SetContent(col, row, char, nil, tcell.StyleDefault)
		col += 1
	}
}
func Print(startRow, startCol, width, height int, ch rune) {
	defStyle := tcell.StyleDefault.Background(tcell.ColorDarkOliveGreen.TrueColor()).Foreground(tcell.ColorWhite)
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
		player1.row -= 2
	} else if key == "Rune[s]" && player1.row+player1.height < screenHeight {
		player1.row += 2
	} else if key == "Up" && player2.row > 0 {
		player2.row -= 2
	} else if key == "Down" && player2.row+player2.height < screenHeight {
		player2.row += 2
	} else if key == "Rune[p]" {
		isGamePaused = !isGamePaused
	}
}
