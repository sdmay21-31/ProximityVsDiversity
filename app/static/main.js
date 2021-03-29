let proxIdsSelected = new Set();
let divIdsSelected = new Set();
let selectedDatabaseId = null;
let dbs = [];
const CHECKBOX = "cb"; const TEXTAREA = "ta";
const TIME = "time", CLUSTER = "cluster";
let inputState = {[TIME]: "", [CLUSTER]: ""};
const PROX = "prox", DIV = "div";
let inputWeightState = {[PROX]: [], [DIV]: []};
const urlGetDb = "databases/";
const urlGetAttrBase = "databases/";
const urlProcess = "process/";
let attrList = ["mass", "luminosity", "hydrogen", "radius"];
var notyf = new Notyf({
  duration: 10000,
  dismissible: true
});
// From Font-Awesome
const xpath = "M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z";
function handleAttrClick(forProx) {
  let arr = forProx ? proxIdsSelected : divIdsSelected;
  return function(label) {
    let taId = label.id.split("_");
    taId[0] = "ta";
    const taIdInd = parseInt(taId[2])
    const textarea = document.querySelector(`#${taId.join("_")}`);
    if (arr.has(taIdInd)) {
      if (proxIdsSelected.size + divIdsSelected.size === 3) {
        document.querySelectorAll(`.attr-item .list-item-cb:disabled:not([id$='_${taIdInd}'])`).forEach(function(e) {
          const eIdInd = parseInt(e.id.split("_")[2]);
          if (!proxIdsSelected.has(eIdInd) && !divIdsSelected.has(eIdInd)) {
            e.removeAttribute("disabled");
          }
        });
      }
      document.querySelector(`.attr-item .list-item-cb:disabled[id$='_${taIdInd}']`).removeAttribute("disabled");
      arr.delete(taIdInd);
      textarea.setAttribute("disabled", "true");
    } else {
      if (proxIdsSelected.size + divIdsSelected.size >= 3) {
        console.error("Why is handleAttrClick called when proxIdsSelected.size + divIdsSelected.size >= 3?");
        return 0;
      }
      arr.add(taIdInd);
      textarea.removeAttribute("disabled");
      document.querySelectorAll(`.attr-item .list-item-cb[id$='_${taIdInd}']:not(:checked)`).forEach(function(e) {
        e.setAttribute("disabled", true);
      });
      if (proxIdsSelected.size + divIdsSelected.size === 3) {
        document.querySelectorAll(".attr-item .list-item-cb:not(:checked)").forEach(function(e) {
          e.setAttribute("disabled", true);
        });
      }
    }
    return 1;
  }
}
function toggleDropdown() {
  document.querySelector(".dropdown-options").classList.toggle("show");
}
function fetchDBsAndPopulateDropdown() {
  fetch(urlGetDb, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function(response) {
    return response.json();
  }).then(function(data) {
    dbs = data.dbs;
    if (dbs) {
      populateDropdown(localStorage.getItem("db"))?.click();
    } else {
      console.error("There was a problem with the dbs array from the database");
    }
  }).catch(function(reason) {
    console.error("There was a problem fetching the database options");
    console.error(reason);
  });
}
function populateDropdown(dbNameFromStorage=null) {
  const dropdown = document.querySelector("#database-options");
  dropdown.innerHTML = "";
  let choice = null;
  dbs.forEach(function(name, ind) {
    const item = document.createElement("p");
    item.id = `option_${ind}`;
    item.classList.add("dropdown-option");
    item.setAttribute("name", name);
    item.onclick = function() { handleDropdownSelection(item) };
    item.appendChild(document.createTextNode(name));
    dropdown.appendChild(item);
    if (dbNameFromStorage && dbNameFromStorage === name) {
      choice = item;
    }
  });
  if (dbNameFromStorage) {
    return choice;
  }
}
function handleHelpTitleClick(helpId) {
  var content = document.getElementById(helpId);
  if(content.style.maxHeight){
    content.style.maxHeight = null;
  } else {
    content.style.maxHeight = content.scrollHeight+"px";
  }
}
function handleDropdownSelection(p) {
  // If everything works correctly, we shouldn't need both these conditions
  // If selecting a selected option causes a "refresh", something went wrong 
  if (p.classList.contains("selected") && selectedDatabaseId === p.id) {
    document.querySelector(".dropdown-options").classList.remove("show");
    return;
  }
  if (p.classList.contains("selected") ^ selectedDatabaseId === p.id) {
    console.error("Error check: element is selected but not stored as selectedDatabaseId");
    return;
  }
  if (selectedDatabaseId) {
    document.querySelector(`#${selectedDatabaseId}`).classList.remove("selected");
  }
  selectedDatabaseId = p.id;
  p.classList.add("selected");
  document.querySelector(".dropdown-button>strong").innerText = `DB: ${p.innerText}`;
  document.querySelector(".dropdown-options").classList.remove("show");
  document.querySelector(".process-button").removeAttribute("disabled");
  proxIdsSelected.clear();
  divIdsSelected.clear();
  document.querySelector('#chart')?.removeAttribute("src");
  inputWeightState = {[TIME]: "", [CLUSTER]: ""};
  if (localStorage.getItem("db") !== p.getAttribute("name")) {
    localStorage.setItem("db", p.getAttribute("name"));
  }
  fetchAndDisplayCardsAttrs();
}
function fetchAndDisplayCardsAttrs() {
  fetch(`${urlGetAttrBase}${dbs[selectedDatabaseId.split("_")[1]]}/attributes/`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function(response) {
    return response.json();
  }).then(function(data) {
    const attrList = data.attrs;
    if (attrList && Array.isArray(attrList) && attrList.length > 0) {
      document.querySelectorAll(".card .attr-item").forEach(e => e.parentNode.removeChild(e));
      document.querySelector("#card-prox").innerHTML += genListItemsForType(attrList, true);
      document.querySelector("#card-div").innerHTML += genListItemsForType(attrList, false);
      inputWeightState[PROX] = new Array(attrList.length).fill("");
      inputWeightState[DIV] = new Array(attrList.length).fill("");
      renderInput(TIME);
      renderInput(CLUSTER);
    } else {
      console.error("There was a problem with the attribute list from the endpoint");
      console.error(data);
    }
  }).catch(function(reason) {
    console.error("There was a problem fetching the attributes");
    console.error(reason);
  });
}
function genListItemsForType(attrArr, isProxAttr) {
  return attrArr.map((attr, ind) => {
    return genListItem(ind, isProxAttr, attr);
  }).join("");
}
function genListItem(id, isProx, attr) {
  // Checks
  if (typeof(id) !== "number" || id % 1 !== 0) { console.error("id should be whole number"); return null; }
  if (typeof(isProx) !== "boolean") { console.error("isProx should be of boolean type"); return null; }
  if (!attr) { console.error("attr is required"); return null; }
  const title = isProx ? "Proximity Attributes" : "Diversity Attributes";
  const type = isProx ? "prox" : "div";
  const rowId = `row_${type}_${id}`;
  const attrProperCase = `${attr.split(" ").filter(v=>v.length).map(capitalizeFirstLetter).join(" ")}`;
  const checkboxId = `cb_${type}_${id}`;
  const textAreaId = `ta_${type}_${id}`;
  const warningId = `w_${type}_${id}`;
  return (`
    <div id="${rowId}" class="list-item attr-item">
      <!-- checkbox & attribute -->
      <div class="list-item-cbattr">
        <label class="list-item-cbattr-label">
          <input id="${checkboxId}" class="list-item-cb" type="checkbox" onclick="handleAttrClick(${isProx})(this)">
          <span><strong style="font-size:1rem;">${attrProperCase}</strong></span>
        </label>
      </div>
      <!-- warning svg -->
      <i id="${warningId}" class="fas fa-exclamation-triangle list-item-warning"></i>
      <!-- input -- if you wanted to accept decimal points event.charCode == 46-->
      <input
        id="${textAreaId}" class="list-item-weight" type="text" placeholder="Weight" disabled=true
        onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"
        oninput="controlInputWeight(event)"
      />
    </div>
  `);
}
function controlInputWeight(event) {
  const [, type, ind] = event.target.id.toLowerCase().split("_");
  const value = event.target.value;
  if (isNaN(value)) {
    event.target.value = inputWeightState[type][ind];
  } else if (parseInt(value) >= 1) {
    inputWeightState[type][ind] = value;
  } else if (value === "") {
    inputWeightState[type][ind] = value;
  } else {
    event.target.value = inputWeightState[type][ind];
  }
}
function renderInput(inputType) {
  const instruction = (inputType === TIME ?
      "Enter a time between 0 and 3000, inclusive" :
      "Enter number of clusters between 1 and 20, inclusive");
  const [min, max] = inputType === TIME ? [0, 3000] : [1, 20];
  const capIT = capitalizeFirstLetter(inputType === TIME ? TIME : CLUSTER);
  const placeholder = inputType === TIME ? capIT : `Number of ${capIT}`;
  document.querySelector(`#input-${inputType}-container`).innerHTML = `
    <p class="input-instruction">${instruction}</p>
    <!-- <div class="input-inner-container">
      <i class="input-warning input-${inputType}-warning fas fa-exclamation-triangle"></i> -->
      <input class="input input-${inputType}" type="text" placeholder="${capIT} (Required)" min=${min} max=${max} inputType="${inputType}"
        onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"
        oninput="controlInput(event)"
      />
    <!-- </div> -->
  `;
  document.querySelector(`#input-${inputType}-container`).classList.add("show");
}
function getInputTypeIgnoreCase(inputType) {
  return inputType.toLowerCase() === TIME ? TIME : CLUSTER;
}
function controlInput(event) {
  const type = getInputTypeIgnoreCase(event.target.getAttribute("inputType"));
  const min = event.target.getAttribute("min");
  const max = event.target.getAttribute("max");
  const value = event.target.value;
  if (isNaN(value)) {
    event.target.value = inputState[type];
  } else if (parseInt(value) >= min && parseInt(value) <= max) {
    inputState[type] = value;
  } else if (value === "") {
    inputState[type] = value;
  } else {
    event.target.value = inputState[type];
  }
}
function process() {
  let errorSomewhere = false;
  if (proxIdsSelected.size + divIdsSelected.size === 0) {
    document.querySelector(".process-attribute-warning").classList.add("show");
    errorSomewhere = true;
  } else if (document.querySelector(".process-attribute-warning").classList.contains("show")) {
    document.querySelector(".process-attribute-warning").classList.remove("show");
  }
  const proxIdsAndWeights = [...proxIdsSelected].map(e => [e, parseInt(document.querySelector(`#row_prox_${e} .list-item-weight`).value)]);
  const divIdsAndWeights = [...divIdsSelected].map(e => [e, parseInt(document.querySelector(`#row_div_${e} .list-item-weight`).value)]);
  const proxNaN = proxIdsAndWeights.filter(function(pair) { return isNaN(pair[1]); });
  const divNaN = divIdsAndWeights.filter(function(pair) { return isNaN(pair[1]); });
  const time = parseInt(document.querySelector(`.input-time`).value);
  const clusters = parseInt(document.querySelector(`.input-cluster`).value);
  document.querySelectorAll(".attr-item .list-item-warning").forEach(function(e) { e.classList.remove("show"); });
  document.querySelector(".input-time").classList.remove("error");
  document.querySelector(".process-time-warning").classList.remove("show");
  document.querySelector(".input-cluster").classList.remove("error");
  document.querySelector(".process-cluster-warning").classList.remove("show");
  if (proxNaN.length + divNaN.length !== 0) {
    proxNaN.forEach(function(pair) {
      document.querySelector(`#row_prox_${pair[0]} .list-item-warning`).classList.add("show");
    });
    divNaN.forEach(function(pair) {
      document.querySelector(`#row_div_${pair[0]} .list-item-warning`).classList.add("show");
    });
    errorSomewhere = true;
  }
  if (isNaN(time)) {
    document.querySelector(".process-time-warning").classList.add("show");
    document.querySelector(".input-time").classList.add("error");
    errorSomewhere = true;
  }
  if (isNaN(clusters)) {
    document.querySelector(".process-cluster-warning").classList.add("show");
    document.querySelector(".input-cluster").classList.add("error");
    errorSomewhere = true;
  }
  if (!errorSomewhere) {
    const db = dbs[selectedDatabaseId.split("_")[1]];
    const proxWeights = proxIdsAndWeights.map(function(pair) { let p = [...pair]; p[0] = attrList[p[0]]; return p; });
    const divWeights = divIdsAndWeights.map(function(pair) { let p = [...pair]; p[0] = attrList[p[0]]; return p; });
    const proxAttrs = proxWeights.map(e => ({ name:e[0], weight:e[1] }));
    const divAttrs = divWeights.map(e => ({ name:e[0], weight:e[1] }));
    // const cookieHalves = `; ${document.cookie}`.split(`; csrftoken=`);
    // const csrf = cookieHalves.length === 2 ? cookieHalves[1].split(";")[0] : null;
    // if (!csrf) {
    //   console.error("CSRF Token not in cookies");
    //   notyf.error("CSRF Token not in cookies");
    //   return;
    // }
    document.querySelector(".process-button-spinner").classList.add("show");
    fetch(urlProcess, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrf,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ db, time, clusters, proxAttrs, divAttrs })
    }).then((response) => {
      return response.json();
    }).then((json) => {
      // remove existing and set new chart image properties: id, maxHeight, src
      let chart = document.querySelector("#chart");
      chart?.parentNode.removeChild(chart);
      chart = document.createElement("img");
      chart.id = "chart";
      chart.style.maxHeight = document.querySelector(".data-input-outer-container").clientHeight;
      chart.src = `data:image/png;base64,${json.chart}`;
      // create a reference image from which to take the width and height to calculate maxHeight
      let referenceImg = new Image();
      referenceImg.onload = () => {
        chart.style.maxWidth = document.querySelector(".data-input-outer-container").clientHeight * referenceImg.width / referenceImg.height;
      }
      referenceImg.src = `data:image/png;base64,${json.chart}`;
      document.querySelector(".chart-container").appendChild(chart);
      // if (json.plotlyData) {
    	//   renderPlotly(json.plotlyData);
      // }
      notyf.success("Processing successful.");
    }).catch(function(reason) {
      console.error("Issue with the POST request.");
      console.error(reason);
      notyf.error("(POST) Not able to process the data.");
    }).finally(function() {
      document.querySelector(".process-button-spinner").classList.remove("show");
    });
  }
}
/**
 * TODO: Extract info from data and add to summary
 */
function createSummary(data, proxWeights, divWeights) {
  const proxList = document.querySelector(".prox-list");
  const divList = document.querySelector(".div-list");
  let li;
  // Just leaving this here for the future
  // `<p class="summary-attr-item"><span class="summary-attr-item-name">mass</span><span class="summary-attr-item-weight">1</span></p>`
  proxList.innerHTML = "";
  divList.innerHTML = "";
  // summary creation for proximity
  if (proxWeights.length === 0) {
    li = document.createElement("li");
    li.appendChild(document.createTextNode("No proximity attribute selected"));
    proxList.appendChild(li);
  } else {
    proxWeights.forEach(function(e) {
      li = document.createElement("li");
      li.appendChild(document.createTextNode(capitalizeFirstLetter(e[0]) + " with a weight of " + e[1]));
      proxList.appendChild(li);
    });
  }
  // summary creation for diversity
  if (divWeights.length === 0) {
    li = document.createElement("li");
    li.appendChild(document.createTextNode("No diversity attribute selected"));
    divList.appendChild(li);
  } else {
    divWeights.forEach(function(e) {
      li = document.createElement("li");
      li.appendChild(document.createTextNode(capitalizeFirstLetter(e[0]) + " with a weight of " + e[1]));
      divList.appendChild(li);				
    });
  }
  // TODO: Extract info from data and add to summary
}
/**
 * TODO: render chart
 */
function renderPlotly(plotlyData) {
  function unpack(rows, key) {
    const ind = dummydata_columns.indexOf(key);
    return rows.map( function(row) { return row[ind]; } );
  }
  const trace1 = {
    x:unpack(plotlyData, 'x1'), y: unpack(plotlyData, 'y1'), z: unpack(plotlyData, 'z1'),
    mode: 'markers',
    marker: {
      size: 12,
      line: {
        color: 'rgba(217, 217, 217, 0.14)',
        width: 0.5
      },
      opacity: 0.8
    },
    type: 'scatter3d'
  };
  const trace2 = {
    x:unpack(plotlyData, 'x2'), y: unpack(plotlyData, 'y2'), z: unpack(plotlyData, 'z2'),
    mode: 'markers',
    marker: {
      color: 'rgb(127, 127, 127)',
      size: 12,
      symbol: 'circle',
      line: {
        color: 'rgb(204, 204, 204)',
        width: 1
      },
      opacity: 0.8
    },
    type: 'scatter3d'
  };
  const data = [trace1, trace2];
  // const data = [trace2];
  const layout = {
    margin: { l: 0, r: 0, b: 0, t: 0 },
    scene: {
      xaxis: { title: 'x Attribute' },
      yaxis: { title: 'y Attribute' },
      zaxis: { title: 'z Attribute' }
    }
  };
  const config = { responsive: true };
  Plotly.newPlot(document.querySelector(".plotly-container"), data, layout, config);
}
function exit(status) {
  // https://stackoverflow.com/a/550583
  // http://kevin.vanzonneveld.net
  // +   original by: Brett Zamir (http://brettz9.blogspot.com)
  // +      input by: Paul
  // +   bugfixed by: Hyam Singer (http://www.impact-computing.com/)
  // +   improved by: Philip Peterson
  // +   bugfixed by: Brett Zamir (http://brettz9.blogspot.com)
  // %        note 1: Should be considered expirimental. Please comment on this function.
  // *     example 1: exit();
  // *     returns 1: null
  var i;
  if (typeof status === 'string') {
    alert(status);
  }
  window.addEventListener('error', function (e) {e.preventDefault();e.stopPropagation();}, false);
  var handlers = [
    'copy', 'cut', 'paste',
    'beforeunload', 'blur', 'change', 'click', 'contextmenu', 'dblclick', 'focus',
    'keydown', 'keypress', 'keyup', 'mousedown', 'mousemove', 'mouseout', 'mouseover', 'mouseup', 'resize', 'scroll',
    'DOMNodeInserted', 'DOMNodeRemoved', 'DOMNodeRemovedFromDocument', 'DOMNodeInsertedIntoDocument', 'DOMAttrModified',
    'DOMCharacterDataModified', 'DOMElementNameChanged', 'DOMAttributeNameChanged', 'DOMActivate', 'DOMFocusIn', 'DOMFocusOut',
    'online', 'offline', 'textInput',
    'abort', 'close', 'dragdrop', 'load', 'paint', 'reset', 'select', 'submit', 'unload'
  ];
  function stopPropagation (e) {
    e.stopPropagation();
    // e.preventDefault(); // Stop for the form controls, etc., too?
  }
  for (i = 0; i < handlers.length; i ++) {
    window.addEventListener(handlers[i], function (e) {stopPropagation(e);}, true);
  }
  if (window.stop) {
    window.stop();
  }
  throw '';
}
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}
fetchDBsAndPopulateDropdown();

// setting a timeout because other renderings are delayed without it
// (new Promise((resolve, reject) => {
//   const script = document.createElement("script");
//   document.body.appendChild(script);
//   script.onload = resolve;
//   script.onerror = reject;
//   script.async = true;
//   script.src = 'static/dummydata.js';
// })).then(() => renderPlotly(dummydata_data));
