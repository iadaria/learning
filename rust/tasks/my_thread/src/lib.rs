use std::thread;
use std::sync::{mpsc, Mutex};
use std::time::Duration;

fn simple_mutex() {
    let m = Mutex::new(5);
    {
        let mut num = m.lock().unwrap();
        *num = 6;
    }

    println!("m = {:?}", m);
}

fn test_channel() {
  let (tx, rx) = mpsc::channel();

    let tx1 = mpsc::Sender::clone(&tx);
    thread::spawn(move|| {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the thread"),
            String::from("of execution")
        ];

        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    thread::spawn(move|| {
        let vals = vec![
            String::from("another"),
            String::from("message"),
            String::from("for"),
            String::from("you")
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Received: {}", received);
    }
}

fn simpleChannelOfFewMessages() {
  let (tx, rx) = mpsc::channel();

  thread::spawn(move|| {
      let vals = vec![
          String::from("hi"),
          String::from("from"),
          String::from("the thread"),
          String::from("of execution")
      ];

      for val in vals {
          tx.send(val).unwrap();
          thread::sleep(Duration::from_secs(1));
      }
  });

  for received in rx {
      println!("Received: {}", received);
  }
}

fn simpleChannel() {
  let (tx, rx) = mpsc::channel();

  thread::spawn(move || {
      let val = String::from("Hi");
      tx.send(val).unwrap();
  });

  let received = rx.recv().unwrap();
  println!("***\nReceived: {}", received);
}

fn vector() {
  let v = vec![1, 2, 3];

  let handle = thread::spawn(move || {
      println!("***\nHere the vector: {:?}", v);
  });

  //drop(v);

  handle.join().unwrap();
}

fn greeting() {
  let handle = thread::spawn(|| {
      for i in 1..10 {
          println!("hi, the number {} is from the spawned thread!", i);
          thread::sleep(Duration::from_millis(1));
      }
  });

  handle.join().unwrap();

  for i in 1..5 {
      println!("hi, the number {} is from the main thread!", i);
      thread::sleep(Duration::from_millis(1));
  }
}