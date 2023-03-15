#[derive(PartialEq, Debug)]
struct Shoe {
  size: u32,
  style: String,
}

fn shoes_in_my_size(shoes: Vec<Shoe>, shoe_size: u32) -> Vec<Shoe> {
  shoes.into_iter()
  .filter(|s| s.size == shoe_size)
  .collect()
}

#[test]
fn filters_by_size() {
  let shoes = vec![
    Shoe { size: 10, style: String::from("sneakers")},
    Shoe { size: 13, style: String::from("sandals")},
    Shoe { size: 10, style: String::from("boots")},
  ];

  let in_my_size = shoes_in_my_size(shoes, 10);

  assert_eq!(
    in_my_size,
    vec![
      Shoe { size: 10, style: String::from("sneakers")},
      Shoe { size: 10, style: String::from("boots")},
    ]
  );
}

/*
Создадим итератор, который будет всегда считать только от 1 до 5.
Сначала мы сделаем структуру для хранения нескольких значений. 
Затем превратим ее в итератор, реализовав типаж Iterator и используя
 эти значения в указанной реализации
*/

struct Counter {
  count: u32, // где мы находимся в процессе перебора значений от 1 до 5
}

impl Counter {
  fn new() -> Counter {
    Counter { count: 0}
  }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
      self.count += 1;

      if self.count < 6 {
        Some(self.count)
      } else {
        None
      }
    }
}

#[test]
fn calling_next_directly() {
  let mut counter = Counter::new();

  assert_eq!(counter.next(), Some(1));
  assert_eq!(counter.next(), Some(2));
  assert_eq!(counter.next(), Some(3));
  assert_eq!(counter.next(), Some(4));
  assert_eq!(counter.next(), Some(5));
  assert_eq!(counter.next(), None);
}

#[test]
fn using_other_iterator_trait_methods() {
  let sum: u32 = Counter::new().zip(Counter::new().skip(1)).map(|(a, b)| a * b).filter(|x| x % 3 == 0).sum();
  assert_eq!(18, sum);
}