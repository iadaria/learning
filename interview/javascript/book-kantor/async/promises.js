
/!** .then **/

/* Here is a reaction to a successfully resolved promise */
function thenResolvePart() {
  // declare a new promise
  let promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("done!", 1000));
  });
  // using .then
  promise.then(
    result => alert(result), // shows "done!" after 1 second
    error => alert(error), //doesn't show
  );
}

function thenRejectionPart() {
  let promise = new Promise((resolve, reject) => {
    setTimeout(() => reject(new Error("Whoops!"), 100));
  });
  promise.then(
    result => alert(result), //doesn't show
    error => alert(error) // shows "Whoops!" after 1 second
  );
}

function thenOnlyResolvePart() {
  let promise = new Promise(resolve => {
    setTimeout(() => resolve("done!"), 1000);
  });
  promise.then(alert); // shows "done!" after 1 second
}

/!** .catch **/

function catchAsThenPart() {
  let promise = new Promise((reslove, reject) => {
    setTimeout(() => reject(new Error("Whoops!"), 1000));
  });
  promise.then(null, alert);
  //or
  promise.catch(alert);
}



/** Executing */

thenResolvePart();
thenRejectionPart();
