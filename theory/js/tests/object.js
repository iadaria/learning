'use strict'

let user1 = {
  name: "Dasha",
  age: 38,
  size: {
    height: 182,
    width: 50
  }
};

let user2 = user1;

let user3 = {};
for(let prop in user1) {
  user3[prop] = user1[prop]
}

let user4 = {...user1};

let user5 = structuredClone(user1);

console.log('user2 === user1', user2 === user1);
console.log('user2.name === user1.name', user2.size === user1.size);

console.log('\nuser3 === user1', user3 === user1)
console.log('\nuser3.size === user1.size', user3.size === user1.size)

console.log('\nuser4 === user1', user4 === user1)
console.log('\nuser4.size === user1.size', user4.size === user1.size)


console.log('\nuser5 === user1', user5 === user1)
console.log('\nuser5.size === user1.size', user5.size === user1.size)