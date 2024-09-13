let obj = {
  name: 'Daria',
  say: () => {
    console.log('hellow')
  },
  eat: function() {
    console.log('I can eat')
  },
  fun() {
    console.log("It's function")
  }
}

obj.sleep = function() {
  console.log('I can sleep')
}

obj.watchTV = function watchTV() {
  console.log('I can watch films')
}

obj.say();
obj.eat();
obj.sleep();
obj.watchTV();
obj.fun();