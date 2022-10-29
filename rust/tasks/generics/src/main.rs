use generics::{Summary, Tweet};

pub fn notify(item: impl Summary) {
    println!("Express news! {}", item.summarize());
}

fn main() {
    let tweet = Tweet {
        username: String::from("Dasha"),
        content: String::from("of course, as you know, maybe, you know, people"),
        reply: false,
        retweet: false,
    };

    println!("1 new tweet: {}", tweet.summarize());
    println!("1 new tweet default: {}", tweet.summarize_default());
}
