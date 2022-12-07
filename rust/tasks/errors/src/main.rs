use std::error::Error;
use std::fs;
//use std::io;
/* use std::io::Read;
use std::fs; */
//use std::io::ErrorKind;

fn main() -> Result<(), Box<dyn Error>> {
    let f = fs::File::open("hello.txt")?;

    Ok(())
    /* let r = read_username_from_file();
    println!("Result: {:?}", r);
    
    let r = read_username_from_file_2();
    println!("Result: {:?}", r);

    let r = read_username_from_file_3();
    println!("Result: {:?}", r); */
    //error_four();
    //error_three();
    //error_two();
    //error_one();
}
/* fn read_username_from_file() -> Result<String, io::Error> {
    let mut f = fs::File::open("hello.txt")?;
    let mut s = String::new();
    f.read_to_string(&mut s)?;
    Ok(s)
}

fn read_username_from_file_2() -> Result<String, io::Error> {
    let mut s = String::new();

    fs::File::open("hello.txt")?.read_to_string(& mut s)?;

    Ok(s)
}

fn read_username_from_file_3() -> Result<String, io::Error> {
    fs::read_to_string("hello.txt")
} */

/* fn read_username_from_file() -> Result<String, io::Error> {
    let f = File::open("hello.txt");

    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    let mut s = String::new();

    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
} */

/* fn error_four() {
    let _f = File::open("hello.txt").expect("It failed to open file");
} */

/* fn error_three() {
    let _f = File::open("hello.txt").unwrap_or_else(|error| {
        if error.kind() == ErrorKind::NotFound {
            File::create("hello.txt").unwrap_or_else(|error| {
                panic!("There is a problem creation the file: {:?}", error);
            })
        } else {
            panic!("There is a problem opening the file: {:?}", error);
        }
    });
} */

/* fn error_two() {
    let f = File::open("hello.txt");
    
    let _f = match f {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create("hello.txt") {
                Ok(fc) => fc,
                Err(e) => panic!("There is a problem of creation a file: {:?}", e),
            },
            other_error => panic!("There is a problem opening the file: {:?}", other_error),
        },
    };
} */

/* fn error_one() {
    panic!("Yes");
} */