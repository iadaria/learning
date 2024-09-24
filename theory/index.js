'use strict';

let worker = {
  someMethod() { return 1 },
  calc(x) {
    return this.someMethod() * x * Math.random()
  }
}

function cachedFunc(func) {
  let cached = new Map();

  return function(x) {
    if (cached.has(x)) { 
      console.log(`get ${x} from cache`)
      return cached.get(x); 
    } 

    let result = func.call(this, x); 
    cached.set(x, result); 

    return result;
  }
}

function client() {
  worker.calc = cachedFunc(worker.calc);

  console.log(worker.calc(1));
  console.log(worker.calc(2));
  console.log(worker.calc(1));

}

client()