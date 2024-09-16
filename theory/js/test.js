'use strict'
let welcome;
{
  function welcome1() {
    console.log("Привет!");
  }
}

{
  welcome = function () {
    console.log("hi")
  }
}
welcome();
welcome1(); // Error: welcome is not defined