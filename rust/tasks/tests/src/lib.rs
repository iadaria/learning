pub fn greeting(name: &str) -> String {
    format!("Hello!")
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn greeting_contains_name() {
        let result = greeting("Dasha");
        assert!(result.contains("Dasha"), "expected `{}`", result);
    }
}
