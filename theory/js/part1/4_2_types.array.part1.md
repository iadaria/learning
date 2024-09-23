# Методы массивов

- `arr.push(...items)` – добавляет элементы в конец,
- `arr.pop()` – извлекает элемент из конца,
- `arr.shift()` – извлекает элемент из начала,
- `arr.unshift(...items)` – добавляет элементы в начало.
- `arr.splice(start[, deleteCount, elem1, ..., elemN])` Метод` arr.splice` – это универсальный «швейцарский нож» для работы с массивами. Умеет всё: добавлять, удалять и заменять элементы. Он изменяет `arr` начиная с индекса `start`: удаляет `deleteCount` элементов и затем вставляет `elem1, ..., elemN` на их место. Возвращает массив из удалённых элементов.
- `arr.slice([start], [end])` 
Он возвращает новый массив, в который копирует все элементы с индекса start до end (не включая end). start и end могут быть отрицательными, в этом случае отсчёт позиции будет вестись с конца массива.
-  `arr.concat` создаёт новый массив, в который копирует данные из других массивов и дополнительные значения.
- Метод `arr.forEach` позволяет запускать функцию для каждого элемента массива.
-  `arr.indexOf(item, from)` ищет `item` начиная с индекса `from` и возвращает номер индекса, на котором был найден искомый элемент, в противном случае -1.
- `arr.includes(item, from)` ищет `item`начиная с индекса `from` и возвращает true, если поиск успешен. Пожалуйста, обратите внимание, что методы используют строгое сравнение ===. Таким образом, если мы ищем false, он находит именно false, а не ноль.
- `find и findIndex/findLastIndex`. Если функция возвращает true, поиск прерывается и возвращается item. Если ничего не найдено, возвращается undefined.
- Метод find ищет один (первый) элемент, который заставит функцию вернуть true.
Если найденных элементов может быть много, можно использовать `arr.filter(fn)`.
- Вызов `arr.sort()` сортирует массив на месте, меняя в нём порядок элементов. Он также возвращает отсортированный массив, но обычно возвращаемое значение игнорируется, так как изменяется сам arr.
- На самом деле от функции сравнения требуется любое положительное число, чтобы сказать «больше», и отрицательное число, чтобы сказать «меньше».
- Метод `arr.reverse` меняет порядок элементов в arr на обратный.
- Метод `str.split(delim)` именно это и делает. Он разбивает строку на массив по заданному разделителю delim.
- Метод `arr.reduceRight` работает аналогично, но проходит по массиву справа налево.
- Почти все методы массива, которые вызывают функции – такие как `find, filter, map`, за исключением метода sort, принимают необязательный параметр `thisArg` для передачи контекста.
- `arr.some(fn)/arr.every(fn)` проверяет массив.
- `arr.fill(value, start, end)` – заполняет массив повторяющимися value, начиная с индекса start до end.
- `arr.copyWithin(target, start, end)` – копирует свои элементы, начиная с позиции start и заканчивая end, в себя, на позицию target (перезаписывая существующие).
- `arr.flat(depth)/arr.flatMap(fn)` создаёт новый плоский массив из многомерного массива.

```js
let arr = ["I", "go", "home"];
delete arr[1]; // удалить "go"
alert( arr[1] ); // undefined
// теперь arr = ["I",  , "home"];
alert( arr.length ); // 3

let element = arr.splice(1, 1); // начиная с индекса 1, удалить 1 элемент
// удалить 3 первых элемента и заменить их другими
arr.splice(0, 3, "Давай", "танцевать");
arr.splice(2, 0, "сложный", "язык"); // добавляем элементы без удаления

arr.slice(1, 3); //(копирует с 1 до 3)

let arr = [1, 2];
arr.concat([3, 4]); // 1,2,3,4

arr.forEach(function(item, index, array) {
  // ... делать что-то с item
});

let arr = [1, 0, false];
arr.includes(1); // true

const arr = [NaN];
alert( arr.indexOf(NaN) ); // -1 (неверно, должен быть 0)
alert( arr.includes(NaN) );// true (верно)

let lengths = ["Бильбо", "Гэндальф", "Назгул"].map(item => item.length);
alert(lengths); // 6,8,6

let arr = [ 1, 2, 15 ];
// метод сортирует содержимое arr
arr.sort();
alert( arr );  // 1, 15, 2

function compare(a, b) {
  if (a > b) return 1; // если первое значение больше второго
  if (a == b) return 0; // если равны
  if (a < b) return -1; // если первое значение меньше второго
}

[1, -2, 15, 2, 0, 8].sort(function(a, b) {
  alert( a + " <> " + b );
  return a - b;
});

arr.sort( (a, b) => a - b ); // Использование стрелочных функций более аккуратно

alert( countries.sort( (a, b) => a > b ? 1 : -1) ); // Andorra, Vietnam, Österreich (неправильно)
alert( countries.sort( (a, b) => a.localeCompare(b) ) ); // Andorra,Österreich,Vietnam (правильно!)
let arr = [1, 2, 3, 4, 5];
arr.reverse();

let arr = 'Вася, Петя, Маша, Саша'.split(', ', 2);
alert(arr); // Вася, Петя

// Разбивка по буквам
let str = "тест";
alert( str.split('') ); // т,е,с,т

let arr = ['Вася', 'Петя', 'Маша'];
let str = arr.join(';') // объединить массив в строку через ;
alert( str ); // Вася;Петя;Маша

let sum = arr.reduce((sum, current) => sum + current, 0);

alert(typeof {}); // object
alert(typeof []); // тоже object

alert(Array.isArray({})); // false
alert(Array.isArray([])); // true
```


```js
let result = arr.find(function(item, index, array) {
  // если true - возвращается текущий элемент и перебор прерывается
  // если все итерации оказались ложными, возвращается undefined
});

let results = arr.filter(function(item, index, array) {
  // если `true` -- элемент добавляется к results и перебор продолжается
  // возвращается пустой массив в случае, если ничего не найдено
});

let result = arr.map(function(item, index, array) {
  // возвращается новое значение вместо элемента
});

let value = arr.reduce(function(accumulator, item, index, array) {
  // ...
}, [initial]);

arr.find(func, thisArg);
arr.filter(func, thisArg);
arr.map(func, thisArg);
```

```js
```

```js
```


```js
```