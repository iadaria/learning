struct ImportantExcept<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Call me Izmail. A few years ago...");
    let first_sentence = novel.split('.').next().expect("Couldn't find '.'");

    let i = ImportantExcept {
        part: first_sentence,
    };
}
