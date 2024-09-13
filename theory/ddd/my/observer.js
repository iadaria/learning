
let observed = {
  state: 1,
  observers: [],
  doSomthing: function(){
    this.state = 2;
    console.log('Observed changed the state to ', this.state);
    this.notify();
  },
  attach: function(observer) {
    this.observers.push(observer)
  },
  detach: function(observer){ 
    this.observers = this.observers.filter(o => o != observer)
  },
  notify: function(){
    for(let observer of this.observers) {
      observer.update(this)
    }
  }
}

let observer1 = {
  update: (observed) => {
    if (observed.state === 2) {
      console.log('Observed1 got state = 2')
    }
  }
}

let observer2 = {
  update: (observed) => {
    if (observed.state === 2 || observed.state ===3 ) {
      console.log('Observed2 got state = 2 or 3')
    }
  }
}

observed.attach(observer1);
observed.attach(observer2);

observed.doSomthing();

observed.detach(observer1);

observed.doSomthing();
