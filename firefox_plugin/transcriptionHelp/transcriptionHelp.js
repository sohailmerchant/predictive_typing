console.log("initializing plugin");
//console.log("Is modal up? "+modalUp);
var textbox;  // set in initializePredBox
var predBox;  // set in initializePredBox
var prevLine = "";
var textboxCursorPos = [30,30];
var normalizeChars = {
    // alifs:
    "أ": "ا",
    "ٱ": "ا",
    "آ": "ا",
    "إ": "ا",
    // alif maqsura:
    "ى": "ي",
    // hamzas:
    "ؤ": "",
    "ئ": "",
    "ء": "",
    // ta marbuta:
    "ة": "ه"
  };

var apiURL = "http://localhost:5000/API/IslamAtlasNgrams?edge=";

/*var edge = "الطول وال";
//let data = await fetch(url)
console.log(api+edge)
fetch(api+edge)
.then(function(resp){
  return resp.json();
}).then(function(data){
  console.log(data);
  apiRes = data;
}).catch(function(error) {
  console.log(error);
});
console.log("data loaded");*/

function lookupInAPI(edge, line_before_cursor){
  fetch(apiURL+edge)
  .then(function(resp){
    if (resp.ok) {
      return resp.json();
    } else {
      throw new Error("No data found");
    }
  }).then(function(r){
    console.log(r);
    if (r.length > 0){
      displayPrediction(r, line_before_cursor);
    } else {
      removeAllChildNodes(predBox);
      predBox.style.display= "none";
    }
  }).catch(function(error) {
    console.log(error);
  });
}


/*
// Load json data from GitHub:
var trigrams = "temp"; // loadJSON("https://raw.githubusercontent.com/pverkind/predictive_typing/main/char_ngrams_in_trigrams.json");
var triFreq = "temp"; // loadJSON("https://raw.githubusercontent.com/pverkind/predictive_typing/main/source_texts_trigram_count.json");
var bigrams = "temp"; // loadJSON("https://raw.githubusercontent.com/pverkind/predictive_typing/main/char_ngrams_in_bigrams.json");
var biFreq = "temp";
loadBiFreq();
loadTriFreq();
loadBigrams();
loadTrigrams();





async function getJsonData(url) {
    let response = await fetch(url);
    let data = await response.json();
    return data;
}

async function loadBiFreq() {
    bigrams = await getJsonData("https://pverkind.github.io/predictive_typing/edge_ngrams_in_bigrams.json");
    console.log("bigrams loaded");
}
async function loadTriFreq() {
    trigrams = await getJsonData("https://pverkind.github.io/predictive_typing/edge_ngrams_in_trigrams.json");
    console.log("trigrams loaded");
}
async function loadBigrams() {
    biFreq = await getJsonData("https://pverkind.github.io/predictive_typing/source_texts_bigrams_normalized_keys.json");
    console.log("biFreq loaded");
}
async function loadTrigrams() {
    triFreq = await getJsonData("https://pverkind.github.io/predictive_typing/source_texts_trigrams_normalized_keys.json");
    console.log("triFreq loaded");
}*/



function resizeTextBox() {
  var textbox = document.getElementById("trans-input");
  //console.log(textbox.style);
  textbox.style.height = "80px";
  //console.log(textbox.style);
}

function initializePredBox(e) {
  if (!document.body.contains(document.getElementById("predBoxDiv"))) {
    console.log("clicked in textbox");
    //console.log(biFreq);
    textbox = document.getElementById("trans-input");
    //console.log(textbox.value);

    // add the predictions box and put it in a wrapper div with the textbox:
    //var wrapper = document.createElement('div');
    //wrapper.setAttribute("id", "predBoxWrapper");
    var predBoxDiv = document.createElement('div');
    predBoxDiv.setAttribute("id", "predBoxDiv");
    predBoxDiv.textContent = "predBox placeholder";
    /*// handle these style elements in css:
    predBoxDiv.style.display = "none";
    predBoxDiv.style.overflow = "scroll";
    predBoxDiv.style.position = "absolute";
    predBoxDiv.style.backgroundColor = "white";
    predBoxDiv.style.boxShadow = "0px 8px 16px 0px rgba(0,0,0,0.2)";*/

    // make sure the predictions are displayed in the same horizontal position as the input text:
    predBoxDiv.style.fontSize = textbox.style.fontSize;
    predBoxDiv.style.transformOrigin = "top right";
    predBoxDiv.style.transform = textbox.style.transform;
    predBoxDiv.style.width = textbox.style.width;

    //wrapper.appendChild(textbox.cloneNode(true));
    //wrapper.appendChild(predBoxDiv);
    //textbox.parentNode.replaceChild(wrapper, textbox);
    //wrapper.style.border = "5px solid red";

    // insert the predBoxDiv after the textbox:
    textbox.parentNode.insertBefore(predBoxDiv, textbox.nextSibling);
    predBox = predBoxDiv;

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
    lookupInAPI("blabla");


    predBox.addEventListener("keydown", handlePredEvents);
  }
}


// handle key events in the input textbox:
function handleInputEvents(e){
  console.log("typed into textbox!");
  initializePredBox(e);
  //cursorPosStart = e.target.selectionStart;
  //cursorPosEnd = e.target.selectionEnd;
  //cursorPos = [cursorPosStart, cursorPosEnd];
  //textboxCursorPos = [e.target.selectionStart, e.target.selectionEnd].sort();
  //console.log("cursorPos: "+cursorPosStart+","+cursorPosEnd);
  //console.log("textboxCursorPos at keyup: ");
  //console.log(textboxCursorPos);
  //let savedCursorPos = [e.target.selectionStart, e.target.selectionEnd];

  var lastKey = e.key;
  console.log("lastKey: "+lastKey);
  if (lastKey === "ArrowDown" ) { // keycode 40
    e.preventDefault();
    predBox.style.display = "block";
    predBox.firstChild.style.backgroundColor = "white";
    predBox.firstChild.nextElementSibling.focus();
    document.activeElement.style.backgroundColor = "lightgrey";
  } else if  (lastKey === "ArrowUp" ) {  // keyCode 38
    e.preventDefault();
    predBox.firstChild.style.backgroundColor = "white";
    predBox.style.display = "block";
    predBox.lastChild.focus();
    document.activeElement.style.backgroundColor = "lightgrey";
    //predBox.firstChild.style.backgroundColor = "lightgrey";
  //} else if (lastKey === 13 ) { // Enter
  } else if (lastKey === "Enter") {
    prevLine = textbox.value;
    console.log("updated prevLine value: "+prevLine);
    // close textBox and open new one
  } else if (lastKey === "Tab") {
    e.preventDefault();
    addToInput(predBox.firstChild.getElementsByTagName("a")[0].textContent);
    predict();
  } else {
    predict();
  }
}

function lastElementSibling(node) {
  return node.parentNode.querySelector(node.nodeName + ':last-of-type');
}

function firstElementSibling(node) {
  return node.parentNode.querySelector(node.nodeName + ':first-of-type');
}

// handle key events in the predBox:
function handlePredEvents(e){
  let lastKey = e.key;
  console.log("lastKey in predBox: "+lastKey);
  /*console.log("currently focussed element: ");
  console.log(document.activeElement);
  console.log("next sibling: ");
  console.log(document.activeElement.nextElementSibling);
  let divs = predBox.getElementsByClassName("pred-div");*/

  if (lastKey === "ArrowUp" ) {
    e.preventDefault();
    document.activeElement.style.backgroundColor = "white";
    let first = firstElementSibling(document.activeElement);
    if (document.activeElement === first) {
      lastElementSibling(document.activeElement).focus();
    } else {
      document.activeElement.previousElementSibling.focus();
    }
    document.activeElement.style.backgroundColor = "lightgrey";

  } else if  (lastKey === "ArrowDown" ) {  // keyCode 40
    e.preventDefault();
    document.activeElement.style.backgroundColor = "white";
    let last = lastElementSibling(document.activeElement);
    if (document.activeElement === last) {
      firstElementSibling(document.activeElement).focus();
    } else {
      document.activeElement.nextElementSibling.focus();
    }
    document.activeElement.style.backgroundColor = "lightgrey";

  } else if (lastKey === "Tab" || lastKey === "Enter") {
    e.preventDefault();
    addToInput(document.activeElement.getElementsByTagName("a")[0].textContent);
    predict();
  } else {
    if (lastKey.length < 3) {
      //addToInput(lastKey);
      console.log("cursor pos to be set in textbox:");
      console.log(textboxCursorPos[0]+","+textboxCursorPos[1]);
      document.getElementById("trans-input").setSelectionRange(textboxCursorPos[0], textboxCursorPos[1]);
      console.log("selection range set");
      document.getElementById("trans-input").focus();
    }
  }
}

function addToInput(s) {
  console.log("textboxCursorPos:"+textboxCursorPos[0]+","+textboxCursorPos[1]);
  let textbox = document.getElementById("trans-input");
  let line = textbox.value;
  textbox.value = line.substring(0, textboxCursorPos[0]) + s.trim() +" " + line.substring(textboxCursorPos[1], line.length);
  textboxCursorPos = [textboxCursorPos[0]+s.length+1, textboxCursorPos[1]+s.length+1];
  textbox.focus();
}

function lookup(tok, edgeNgrams, freq) {
  /* The lookup goes in two stages:
  1. first the function checks whether the last two tokens are in the edgeNgrams dictionary;
     the keys in this dictionary are normalized, and the values are the characters
     that together with the keys form the full ngrams.
  2. in the next stage, the script checks in the freq dictionary
     how many times each of the full ngrams that agree with this normalized keys
     were found in the source texts.
  Finally, the function returns an array of arrays (prediction, count)
  */
  //console.log("starting lookup");
  if (!(normalize(tok) in edgeNgrams)){
    return [];
  }
  var n = edgeNgrams[normalize(tok)];
  console.log("number of edgeNgrams found:"+n.length);
  console.log(n);
  //console.log("Lookup found "+n.length+" results")
  var r = new Array();
  for (let i=0; i<n.length; i++) {
    //var nxt = n[i].substring(tok.length, n[i].length);
    var nxt = n[i];
    if (nxt !== "") {
      console.log("nxt: "+nxt);
      var normalizedKey = normalize(tok+nxt);
      console.log("normalizedKey: "+normalizedKey);
      for (const k in freq[normalizedKey]) {
        console.log("    const k in freq[normalizedKey]: "+k);
        r.push([ k.substring(tok.length, k.length), freq[normalizedKey][k] ]);
      }
    }

  }
  /*if (r.length > 0) {
    displayPrediction(r);
  } else {
    console.log("nothing to display");
    predBox.style.display = "none";
  }*/
  return r;
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function displayPrediction(pred, prev){
  console.log("displaying prediction");
  // empty predBox's content:
  //predBox.innerHtml = "";
  removeAllChildNodes(predBox);

  // create span that contains the text of the line, in grey:
  var prevSpan = document.createElement("span");
  prevSpan.className = "prev";
  prevSpan.style.color = "lightgrey";
  prevSpan.textContent = prev;

  //prev = '<span style="color: lightgrey;">'+prev+'</span>';

  // add predictions to predBox:
  for (let i=0; i < pred.length; i++) {
    //console.log(i);
    //console.log(pred[i][0]);
    let predDiv = document.createElement("div");
    predDiv.id = "pred"+i;
    predDiv.className = "pred-div";
    predDiv.style.display = "block";
    predDiv.style.direction = "rtl";
    predDiv.style.textAlign = "right";
    predDiv.tabIndex = "-1";  // make div focussable
    if (i === 0) {
      predDiv.style.backgroundColor = "lightgrey";
    }
    // predDiv.textContent = pred[i];
    // predDiv.innerHtml = prev+pred[i][0];
    let pred_a = document.createElement("a");
    pred_a.textContent = pred[i][0];
    predDiv.appendChild(prevSpan.cloneNode(true));
    predDiv.appendChild(pred_a);
    predBox.appendChild(predDiv);
  }
  // make predBox visible:
  predBox.style.display = "block";
} 

function normalize(s) {
  let re = new RegExp(Object.keys(normalizeChars).join("|"), "g");
  s = s.normalize("NFKC");
  s = s.replace(re, function(m) {
    return normalizeChars[m];
  });
  return s
}


function predict(){
  var textbox = document.getElementById("trans-input");
  console.log("starting prediction");
  console.log("textboxCursorPos: ");
  console.log(textboxCursorPos);

  var line = textbox.value;
  console.log(line);
  var line_before_cursor = line.substring(0,textboxCursorPos[0]);
  var line_after_cursor = line.substring(textboxCursorPos[1], line.length);
  console.log(line_before_cursor + " - " + line_after_cursor);
  console.log("prevLine in array:");
  console.log([prevLine]);
  if (prevLine.length > 0) {
    var lastLines = prevLine + " " + line_before_cursor;
  } else {
    var lastLines = line_before_cursor;
  }
  if (lastLines.length < 5) {
    console.log("less than 5 characters. Waiting for more characters before starting prediction");
    return;
  }
  lastTokens = lastLines.trim().split(" ");
  //console.log("line: "+line);
  //console.log(lastTokens);

  var lastTok = lastTokens[lastTokens.length-1];
  var lastTwo = lastTokens[lastTokens.length-2] + " " + lastTok;

  console.log("lastTok: "+lastTok);
  console.log("lastTwo: "+lastTwo);
  console.log([lastTokens, lastTok, lastTwo]);

  lookupInAPI(lastTwo, line_before_cursor);

  /*var r3 = lookup(lastTwo, trigrams, triFreq);
  console.log("found "+r3.length+" trigram results for "+lastTwo);
  console.log(r3);

  var r2 = lookup(lastTwo, bigrams, biFreq);
  console.log("found "+r2.length+" bigram results for"+lastTwo);
  console.log(r2);

  //var r = new Set([...r2,...r3]); // union
  //r = Array.from(r);
  var r = [... new Set([...r2,...r3])]; // union
  console.log("found "+r.length+" bi-and trigram results for "+lastTwo);
  console.log(r);
  if (r.length > 0){
    r.sort(function(a,b){
      return a[1] - b[1];
    }).reverse();
    //return r;
    displayPrediction(r, line_before_cursor);
  } else {
    predBox.style.display= "none";
  }*/
}

// add click + key event listeners to the transcription input
document.addEventListener('mouseup',function(e){
  //console.log("clicked e.target.id "+e.target.id);
  if (e.target && e.target.id=='trans-input'){
    //console.log("CLICKED e.target.id "+e.target.id);
    initializePredBox(e);
    textbox.focus();
  }
});
document.addEventListener('keyup',function(e){
  //if (e.key === "Tab" || e.key === "ArrowUp" || e.key === "ArrowDown") {
  console.log(e.key);
  console.log(e.which);
  if (e.key == "ArrowDown" || e.key == "ArrowUp" || e.key == "Tab") {
    e.preventDefault();
    e.stopPropagation();
    console.log("tried to stop keyup event from propagating");
  }
  if (e.target && e.target.id=='trans-input'){
    handleInputEvents(e);
  }
}, true);
document.addEventListener('keydown',function(e){
  //if (e.key === "Tab" || e.key === "ArrowUp" || e.key === "ArrowDown") {
  console.log(e.key);
  console.log(e.which);
  if (e.key == "ArrowDown" || e.key == "ArrowUp" || e.key == "Tab") {
    e.preventDefault();
    e.stopPropagation();
    console.log("tried to stop keydown event from propagating");
  }
  if (e.target && e.target.id=='trans-input'){
    textboxCursorPos = [e.target.selectionStart, e.target.selectionEnd].sort();
    console.log("textboxCursorPos at keydown: ");
    console.log(textboxCursorPos);
  }
}, true);

document.addEventListener('keypress',function(e){
  //if (e.key === "Tab" || e.key === "ArrowUp" || e.key === "ArrowDown") {
  if (e.key === "ArrowDown") {
    e.preventDefault();
    e.stopPropagation();
    console.log("tried to stop keypress event from propagating");

  }
}, true);
