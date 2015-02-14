function calculate(evt) {
  var button = evt.target;
  var resultDisplay = document.getElementById('result');
  resultDisplay.className = "result hidden";

  // P tag may have been clicked
  if (button.tagName === 'BUTTON') {
    var frm = document.getElementById('calcform');
    var a = parseFloat(frm.input_a.value, 10);
    var b = parseFloat(frm.input_b.value, 10);
  }
  else {
    return;
  }

  // Numbers only please
  if (isNaN(a) || isNaN(b) || !isFinite(a) || !isFinite(b)) {
    result = "Numbers Only Please";
    resultDisplay.className += ' error';
  }
  else {
    switch (button.name) {
      case "addbutton":
        result = a + b;
        break;
      case "multbutton":
        result = a * b;
        break;
      case "divbutton":
        result = a / b;
        break;        
    }      
  }
  resultDisplay.classList.remove("hidden");
  resultDisplay.textContent = result;
}

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("button_wrapper").onclick = calculate;
});
