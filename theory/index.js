'use strict';

let f = function func(ha) {
  console.log('ha')
  if (!ha) return
  func()
}

function client() {
f('ha')

}

client()