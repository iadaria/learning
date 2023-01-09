use std::{env, process};

use minigrep::{run, Config};

fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::new(&args).unwrap_or_else(|err| {
        println!("There is a problem in the parsing the arguments: {}", err);
        process::exit(1);
    });

    println!("Searching '{}'", config.query);
    println!("In the file '{}'", config.filename);

    if let Err(e) = run(config) {
        println!("Something went wrong when reading the file {}", e);
        process::exit(1);
    }
}
