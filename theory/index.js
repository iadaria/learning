

function client() {
 let user = {
  name: "Dasha",
  age: 38
 }

 console.log(user)

 for(let key in user) {
  console.log(key)
  console.log(user[key])
 }
}
client();