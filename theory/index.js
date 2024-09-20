function Person() {
  this.name = "Das";
  this.age = 38;
  this.walk = function () {
    confirm.log(this.name + ' can walk')
  }
}

function client() {
  let person = new Person();
  console.log(person)
  console.log('Person.walk', person.walk.toString())
  //console.log('singleton1 === singleton2', sheep1 === sheep2)

  let clone = Object.create(person);
  console.log('clone',clone)
}

client();