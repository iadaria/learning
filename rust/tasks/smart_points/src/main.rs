enum List {
    Cons(i32, Box<List>),
    Nil
}

enum ListRc {
    ConsRc(i32, Rc<ListRc>),
    NilRc,
}

use std::ops::Deref;
use crate::List::{Cons, Nil};
use std::rc::Rc;
use crate::ListRc::{ConsRc, NilRc};

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
    let w = MyBox::new(x);

    println!("x = {}", x);
    println!("y = {}", y);
    println!("*y = {}", *y);
    println!("*z = {}", *z);
    println!("*w = {}", *w);


    assert_eq!(5, x);
    assert_eq!(5, *y);
    assert_eq!(5, *z);
    assert_eq!(5, *w);

    /* let a = Cons(5, Box::new(Cons(10,Box::new(Nil))));
    let b = Cons(3, Box::new(a));
    let c = Cons(4, Box::new(a)); */

    let a = Rc::new(ConsRc(5, Rc::new(ConsRc(10, Rc::new(NilRc)))));
    println!("the count after creating a = {}", Rc::strong_count(&a));
    let b = ConsRc(3, Rc::clone(&a));
    println!("the count after creating b = {}", Rc::strong_count(&a));
    {
        let c = ConsRc(3, Rc::clone(&a));
        println!("the count after creating c = {}", Rc::strong_count(&a));
    }
    println!("the count after existing th scope = {}", Rc::strong_count(&a));

    //println!("hi there")
}
