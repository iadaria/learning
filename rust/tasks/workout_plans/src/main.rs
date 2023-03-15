use std::{collections::HashMap, thread, time::Duration};

struct Cacher<T>
where
    T: Fn(u32) -> u32,
{
    calculation: T,
    value: Option<u32>,
    value_two: HashMap<u32, u32>,
}

impl<T> Cacher<T>
where
    T: Fn(u32) -> u32,
{
    fn new(calculation: T) -> Cacher<T> {
        Cacher {
            calculation,
            value: None,
            value_two: HashMap::new(),
        }
    }

    fn value_two(&mut self, arg: u32) -> u32 {
        for (key, value) in &self.value_two {
            //if key == &arg {
            if *key == arg {
                return value.clone();
            }
        }
        let v = (self.calculation)(arg);
        self.value_two.insert(arg, v);
        v
    }

    fn value(&mut self, arg: u32) -> u32 {
        match self.value {
            Some(v) => v,
            None => {
                let v = (self.calculation)(arg);
                self.value = Some(v);
                v
            }
        }
    }
}

#[test]
fn call_with_different_values() {
    let mut c = Cacher::new(|a| a);
    let v1 = c.value(1);
    let v2 = c.value(2);

    assert_eq!(v2, 2);
    assert_ne!(v1, v2);
}
#[test]
fn call_with_different_values_two() {
    let mut c = Cacher::new(|a| a);
    let v1 = c.value_two(1);
    let v2 = c.value_two(2);

    assert_eq!(v2, 2);
    assert_ne!(v1, v2);
}

fn main() {
    let simulated_user_specified_value = 10;
    let simulated_random_number = 7;

    generate_workout(simulated_user_specified_value, simulated_random_number);
}

fn generate_workout(intensity: u32, random_number: u32) {
    let mut expensive_result = Cacher::new(|num: u32| -> u32 {
        println!("calculating slowly...");
        thread::sleep(Duration::from_secs(2));
        num
    });

    if intensity < 25 {
        println!("Today do {} push-ups!", expensive_result.value(intensity));
        println!("Today do {} sit-ups!", expensive_result.value(intensity));
    } else {
        if random_number == 3 {
            println!("Today do break-up! Drink more water!");
        } else {
            println!(
                "Today go for a run {} minutes!",
                expensive_result.value(intensity)
            );
        }
    }
}

/* fn simulated_expensive_calculation(intensity: u32) -> u32 {
} */
