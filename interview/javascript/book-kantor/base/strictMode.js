function strict() {
  'use strict';
  
  function nested() {
    hi = 'hello';
    console.log(hi);
  }
  nested();
}
strict();

process.exit(0);

function strictModule() {
  hi = 'hello'; 
  console.log(hi);
}

strictModule();

process.exit(0);


hi = 1;
'use strict';
console.log(hi);

process.exit(0);


setTimeout('"use strict"; let x = 10; y3 = 20;', 1000);

let code = '"use strict"; let x = 10; y = 20;'

eval(code)

let func = new Function('"use strict"; let x = 10; y2 = 20;');

func();