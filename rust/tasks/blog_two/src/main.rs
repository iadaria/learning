use blog_two::Post;

fn main() {
  let mut post = Post::new();

  post.add_text("Today I ate salad for lunch");
  
  let post = post.request_review();

  let post = post.approve();

  assert_eq!("Today I ate salad for lunch", post.content());
}