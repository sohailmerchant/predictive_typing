//var modalUp = false;
//console.log("Is modal up? "+modalUp);
var textbox;  // set in initializePredBox
var predBox;  // set in initializePredBox
var prevline = "";

function resizeTextBox() {
  var textbox = document.getElementById("trans-input");
  //console.log(textbox.style);
  textbox.style.height = "80px";
  //console.log(textbox.style);
}

function initializePredBox(e) {
  //console.log("clicked in textbox");
  //console.log("Is modal up? "+modalUp);
  textbox = document.getElementById("trans-input");
  //console.log(textbox.value);

  // add the predictions box and put it in a wrapper div with the textbox:
  var wrapper = document.createElement('div');
  wrapper.setAttribute("id", "predBoxWrapper");
  var predBoxDiv = document.createElement('div');
  predBoxDiv.setAttribute("id", "predBox");
  predBoxDiv.textContent = "predBox placeholder";
  wrapper.appendChild(textbox.cloneNode(true));
  wrapper.appendChild(predBoxDiv);
  textbox.parentNode.replaceChild(wrapper, textbox);
  //wrapper.style.border = "5px solid red";
  predBox = predBoxDiv;
  //console.log("Is modal up now? "+modalUp);

  // enable focus move with arrow keys:
  /*$(document).keydown(function(e){  // http://jsfiddle.net/uJ4PJ/, https://stackoverflow.com/questions/11088674/shift-focus-with-arrow-keys-in-javascript/11088844
    //predBox.addEventListener("keydown", function(e){
    if (e.keyCode == 39) {
      $(".move:focus").prev().focus();
    } else if (e.keyCode == 37) {
      $(".move:focus").prev().focus();
    }
  }*/

  // set the height of the text box to 80px to make the diacritics visible:
  resizeTextBox();
  console.log(predBox.textContent);

  // make sure this is not done again on the same text input:
  //modalUp = true;
}

function getCursorPos(e) {
  return e.target.selectionStart;
}

function handleInputEvents(e){
  if (!document.body.contains(document.getElementById("predBox"))) {
    initializePredBox(e);
  }
  var cursorPos = getCursorPos(e);
  //console.log("cursorPos: "+cursorPos);

}

// add click + key event listeners to the transcription input
document.addEventListener('mouseup',function(e){
  //console.log("clicked e.target.id "+e.target.id);
  if (e.target && e.target.id=='trans-input'){
    //console.log("CLICKED e.target.id "+e.target.id);
    handleInputEvents(e);
  }
});
document.addEventListener('keyup',function(e){
  if (e.target && e.target.id=='trans-input'){
    handleInputEvents(e);
  }
});
