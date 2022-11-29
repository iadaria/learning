use std::fs::File;

fn main() {
    // error_one();
    error_two();
}

/* fn error_one() {
    panic!("Yes");
} */

fn error_two() {
    let _f = File::open("hello.txt");
    File::open(path)
}