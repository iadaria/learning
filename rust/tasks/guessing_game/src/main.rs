use rand::Rng;
use std::cmp::Ordering;
use std::io;

/* fn print_type_of<T>(_: &T) {
  print!("{}", std::any::type_name::<T>())
} */

pub struct Guess {
    value: i32,
}

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 || value > 100 {
            panic!(
                "The scrent number have to between 1 and 100, but got {}",
                value
            );
        }

        Guess { value }
    }

    pub fn value(&self) -> i32 {
        self.value
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn greater_than_100() {
        Guess::new(200);
    }
}

fn main() {
    println!("Guess the number!");

    let secret_number = rand::thread_rng().gen_range(1, 101);
    println!("The secret number is {}", secret_number);

    loop {
        println!("Please, enter your option!");

        let mut value = String::new();

        io::stdin()
            .read_line(&mut value)
            .expect("Can't read the row");

        let value: i32 = match value.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
        //.expect("Please, enter a digit");
        //print_type_of(&guess);

        /* if guess < 1 || guess > 100 {
          println!("The secret number is between 1 and 100");
          continue
        }*/
        println!("You make the number: {} ", value);

        let mut guess = Guess::new(value);

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small number"),
            Ordering::Greater => println!("Too large number"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
