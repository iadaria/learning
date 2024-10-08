// inheritance

pub trait Draw {
  fn draw(&self);
}

// Box<dyn Draw> является типажным объектом и замещает любой тип внутри Box, реализующий типаж Draw
pub struct Screen {
  pub components: Vec<Box<dyn Draw>>,
}

impl Screen {
  pub fn run(&self) {
    for component in self.components.iter() {
      component.draw()
    }
  }
}

pub struct Button {
  pub width: u32,
  pub height: u32,
  pub label: String,
}

impl Draw for Button {
  fn draw(&self) {
    // код для фактической отрисовки кнопки
  }
}

/* * Альтернатива * * */
pub struct ScreenTwo<T: Draw> {
  pub components: Vec<T>,
}

impl<T> ScreenTwo<T>
  where T: Draw {
    pub fn fun(&self) {
      for component in self.components.iter() {
        component.draw();
      }
    }
  }
/* * * * * * * * */

// Encapsulation

pub struct AveragedCollection {
    list: Vec<i32>,
    average: f64,
}

impl AveragedCollection {
    pub fn add(&mut self, value: i32) {
        self.list.push(value);
        self.update_average();
    }

    pub fn remove(&mut self) -> Option<i32> {
        let result = self.list.pop();
        match result {
            Some(value) => {
                self.update_average();
                Some(value)
            }
            None => None,
        }
    }

    pub fn average(&self) -> f64 {
        self.average
    }

    fn update_average(&mut self) {
        let sum: i32 = self.list.iter().sum();
        self.average = sum as f64 / self.list.len() as f64;
    }
}

pub fn encapsulation() {
    let mut ac = AveragedCollection {
        list: vec![],
        average: 0.0,
    };

    println!("Average: {}", ac.average);

    ac.add(3);
    ac.add(3);

    println!("Length: {}, Average: {}", ac.list.len(), ac.average);
}
