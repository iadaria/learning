function Product() {
  this.price = 0;
  this.actions = [];
}

Product.prototype.setBasePrice = function(val) {
  this.price = val;
  this.notifyAll();
};

Product.prototype.register = function(observer) {
  this.actions.push(observer);
};

Product.prototype.unregister = function(observer) {
  this.actions = this.actions.filter(function(o) {
    return o != observer
  })
};

Product.prototype.notifyAll = function() {
  return this.actions.forEach(function(o) {
    o.update(this);
  }.bind(this))
};

let fees = {
  update: function(product) {
    product.price = product.price * 1.2;
  }
};

let proft = {
  update: function(product) {
    product.price = product.price * 2;
  }
}

module.exports = [Product, fees, proft];

// observed.attach(observer1);
// observed.attach(observer2);
// observed.doSomthing();
// observed.detach(observer1);
// observed.doSomthing();
