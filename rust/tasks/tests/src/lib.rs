pub fn greeting(name: &str) -> String {
    format!("Hello! {}", name)
}

pub struct Guess {
    value: i32,
}

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 {
            panic!(
                "The scrent number have to be more or equal 1, but got {}",
                value
            );
        } else if value > 100 {
            panic!(
                "The scrent number have to be less or equal 100, but got {}",
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
    fn greeting_contains_name() {
        let result = greeting("Dasha");
        assert!(result.contains("Dasha"), "expected `{}`", result);
    }
    #[test]
    #[should_panic(expected = "The scrent number have to be less or equal 100, but got 100")]
    fn greater_than_100() {
        Guess::new(200);
    }

    #[test]
    fn it_works() -> Result<(), String> {
        if 2 + 3 == 4 {
            Ok(())
        } else {
            Err(String::from("2 + 3 != 4 "))
        }
    }
}
