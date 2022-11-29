package main

import "fmt"

type PVehicle interface {
	move()
}

type PCar struct{ model string }
type PAircraft struct{ model string }

func (c PCar) move() {
	fmt.Println(c.model, "is driving")
}

func (a PAircraft) move() {
	fmt.Println(a.model, "is flying")
}

func polymorphismMain() {
	tesla := PCar{"Tesla"}
	volvo := PCar{"Volvo"}
	boeing := PAircraft{"Boeing"}

	vehicles := [...]PVehicle{tesla, volvo, boeing}
	for _, vehicle := range vehicles {
		vehicle.move()
	}
}
