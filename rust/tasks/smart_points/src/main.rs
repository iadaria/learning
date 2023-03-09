enum List {
    Cons(i32, Box<List>),
    Nil
}

use std::ops::Deref;
use crate::List::{Cons, Nil};

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;
    
    fn deref(&self) -> &T {
        &self.0
    }
}

fn main() {
    let x = 5;
    let y = &x;
    let z = Box::new(x);
    let a = MyBox::new(x);

    println!("x = {}", x);
    println!("y = {}", y);
    println!("*y = {}", *y);
    println!("*z = {}", *z);
    println!("*a = {}", *a);


    assert_eq!(5, x);
    assert_eq!(5, *y);
    assert_eq!(5, *z);
    assert_eq!(5, *a);

    let list = Cons(1, Box::new(Cons(2,Box::new(Cons(3, Box::new(Nil))))));
    //println!("hi there")
}
