use generics::{Summary, Tweet};

pub fn notify(item: impl Summary) {
    println!("Express news! {}", item.summarize());
}

fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("horse_ebooks"),
        content: String::from("of course, how are you"),
        reply: false,
        retweet: false,
    }
}

fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for item in list.iter() {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn largest_two<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];

    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 54];

    let result = largest(&number_list);
    println!("\nThe biggest digit is {}", result);

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest(&char_list);
    println!("The lagest symbol is {}\n", result);

    let tweet = Tweet {
        username: String::from("Dasha"),
        content: String::from("of course, as you know, maybe, you know, people"),
        reply: false,
        retweet: false,
    };

    println!("\n1 new tweet: {}", tweet.summarize());
    println!("1 new tweet default: {}\n", tweet.summarize_default());

    returns_summarizable();
}
