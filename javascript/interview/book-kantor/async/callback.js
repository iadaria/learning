// 1 part
function loadScript(src, callback) {
  let script = document.createElement('script');
  script.src = src;
  // 2 part
  script.onload = () => callback(script);
  document.head.append(script);
}

loadScript('async/script.js', function () {
  newFunction();
});
