function firstPart() {
  // 1 part
  function loadScript(src, callback) {
    let script = document.createElement("script");
    script.src = src;
    document.head.append(script);
  }

  loadScript("async/script.js", function () {
    newFunction(1);

    loadScript("async/script2.js", function () {
      newFunctionTwo(2);

      loadScript("async/script3.js", function () {
        newFunction(3);

        loadScript("async/script4.js", function () {
          newFunction(4);

          loadScript("async/script5.js", function () {
            newFunction(5);
          });
        }); // the fifth loadScript
      }); // the third loadScript
    }); // the second loadScript
  }); // the first loadScript
}

function handlingErrors() {
  function loadScript(src, callback) {
    let script = document.createElement("script");
    script.src = src;
    // 2 part
    script.onload = () => callback(null, script);
    scirpt.onerror = () => callback(new Error(`script load error for ${src}`));
    //
    document.head.append(script);
  }

  // how to use
  loadScript("async/script.js", function(error, script) {
    if (error) {
      console.log('[script.js]', { error });
    } else {
      // script loaded successfully
      newFunction(1);
    }
  });

  // Pyramid of Doom
  loadScript("async/script.js", function(error, script) {
    if (error) {
      console.log('[script.js]', { error });
    } else {
      newFunction(1);

      loadScript("async/script1.js", function(error, script) {
        if (error) {
          console.log('[script1.js]', { error });
        } else {
          newFunction(2);

          loadScript("async/script3.js", function(error, script) {
            if (error) {
              console.log('[script3.js]', { error });
            } else {
              newFunction(3);
              //...continue after all scripts are loaded
            }
          });
        }
      });
    }
  });

  // standalone functions
  loadScript('async/1.js', step1);

  function step1(error, script) {
    if (error) {
      console.log('[async/1.js]', { error });
    } else {
      newFunction(1);
      loadScript('async/2.js', step2);
    }
  }

  function step2(error, script) {
    if (error) {
      console.log('[asycn/2.js]', { error });
    } else {
      newFunction(2);
      loadScript('async/3.js', step3);
    }
  }

  function step3(error, script) {
    if (error) {
      console.log('[asycn/3.js]', { error });
    } else {
      newFunction(2);
      loadScript('async/4.js', step4);
    }
  }

}

