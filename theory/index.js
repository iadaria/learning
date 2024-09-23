function pow(x, n) {
  let result = 1;
  for(let i = 0; i < n; i++) {
    result *= x;
  }
  return result;
}

function pow2(x, n) {
  return (n === 1) ? x: x * pow2(x, n - 1)
}

function clien() {
  let result = pow(2, 3);

  console.log(result)

  let result2 = pow2(2, 3);

  console.log(result2)
}

clien()