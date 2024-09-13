function Singleton() {

  if (typeof Singleton.instance === 'object') {
    return Singleton.instance;
  }

  Singleton.instance = this;
  return this;
}


let person = new Singleton();
let person2 = new Singleton();

console.log('person = person2', person === person2)