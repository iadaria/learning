function Pasta() {
  this.price = 0;
}
Pasta.prototype.getPrice = function() {
  return this.price;
}

function Penne() {
  this.price = 0;
}
Penne.prototype = Object.create(Pasta.prototype);

function SauceDecorator(pasta) {
  this.pasta = pasta;
}

SauceDecorator.prototype.getPrice = function() {
  return this.pasta.getPrce() + 5;
}

function CheeseDecorator(pasta) {
  this.pasta = pasta
}

CheeseDecorator.prototype.getPrice = function() {
  return this.pasta.getPrice + 3;
}

module.export = [Penne, SauceDecorator, CheeseDecorator]