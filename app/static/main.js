let proxIdsSelected = new Set();
let divIdsSelected = new Set();
let selectedDatabaseId = null;
let dbs = [];
let prevInputValue = "";
const CHECKBOX = "cb"; const TEXTAREA = "ta";
const urlGetDb = "databases/";
const urlGetAttrBase = "databases/";
const urlProcess = "process/";
let attrList = ["mass", "luminosity", "hydrogen", "radius"];
window.proxIdsSelected = proxIdsSelected;
window.divIdsSelected = divIdsSelected;
window.selectedDatabaseId = selectedDatabaseId;
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
    console.log(response)
    return response.json();
  }).then(function(data) {
    dbs = data.dbs;
    if (dbs) {
      populateDropdown();
    } else {
      console.error("There was a problem with the dbs array from the database");
    }
  }).catch(function(error) {
    console.error("There was a problem fetching the database options");
  });
}
function populateDropdown() {
  const dropdown = document.querySelector("#database-options");
  dropdown.innerHTML = "";
  dbs.forEach(function(name, ind) {
    const item = document.createElement("p");
    item.id = `option_${ind}`;
    item.classList.add("dropdown-option");
    // item.onclick = handleDropdownSelection.bind(item);
    item.onclick = function() { handleDropdownSelection(item) };
    item.appendChild(document.createTextNode(name));
    dropdown.appendChild(item);
  });
}
function handleDropdownSelection(p) {
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
  prevInputValue = "";
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
      renderInputTime();
    } else {
      console.error("There was a problem with the attribute list from the endpoint");
      console.error(data);
    }
  }).catch(function(reason) {
    console.error("There was a problem fetching the attributes");
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
  const attrProperCase = `${attr.split(" ").filter(v=>v.length).map(v=>`${v[0].toUpperCase()}${v.slice(1)}`).join(" ")}`;
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
      />
    </div>
  `);
}
function renderInputTime() {
  document.querySelector("#input-time-container").innerHTML = `
    <p class="input-time-instruction">Enter a time between 0 and 3000, inclusive</p>
    <div class="input-time-inner-container">
      <i class="input-time-warning fas fa-exclamation-triangle"></i>
      <input class="input-time" id="input-time" type="text" placeholder="Time (Required)"
        onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"
        oninput="controlInputTime(event)"
      />
    </div>
  `;
  document.querySelector("#input-time-container").classList.add("show");
}
function controlInputTime(event) {
  const value = event.target.value;
  if (parseInt(value) >= 0 && parseInt(value) <= 3000) {
    prevInputValue = value;
  } else if (value === "") {
    prevInputValue = value;
  } else {
    event.target.value = prevInputValue;
  }
}
function process() {
  let errorSomewhere = false;
  if (proxIdsSelected.size + divIdsSelected.size === 0) {
    document.querySelector(".process-warning").classList.add("show");
    errorSomewhere = true;
  } else if (document.querySelector(".process-warning").classList.contains("show")) {
    document.querySelector(".process-warning").classList.remove("show");
  }
  const proxIdsAndWeights = [...proxIdsSelected].map(e => [e, parseInt(document.querySelector(`#row_prox_${e} .list-item-weight`).value)]);
  const divIdsAndWeights = [...divIdsSelected].map(e => [e, parseInt(document.querySelector(`#row_div_${e} .list-item-weight`).value)]);
  const proxNaN = proxIdsAndWeights.filter(function(pair) { return isNaN(pair[1]); });
  const divNaN = divIdsAndWeights.filter(function(pair) { return isNaN(pair[1]); });
  const time = parseInt(document.querySelector(".input-time").value);
  document.querySelectorAll(".attr-item .list-item-warning").forEach(function(e) { e.classList.remove("show"); });
  document.querySelector(".input-time-warning").classList.remove("show");
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
    document.querySelector(".input-time-warning").classList.add("show");
    errorSomewhere = true;
  }
  if (!errorSomewhere) {
    const db = dbs[selectedDatabaseId.split("_")[1]];
    const proxWeights = proxIdsAndWeights.map(function(pair) { let p = [...pair]; p[0] = attrList[p[0]]; return p; });
    const divWeights = divIdsAndWeights.map(function(pair) { let p = [...pair]; p[0] = attrList[p[0]]; return p; });
    const proxAttrs = proxWeights.map(e=>({name:e[0],weight:e[1]}));
    const divAttrs = divWeights.map(e=>({name:e[0],weight:e[1]}));
    fetch(urlProcess, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrf, 
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ db, time, proxAttrs, divAttrs })
    }).then((response) => {
      return response.json();
    }).then((json) => {
      console.log(json);
      document.querySelector('#chart').src = `data:image/png;base64,${json.chart}`
      if (json.data) {
    	  createSummary(json.data);
      }
      createSummary(undefined, proxWeights, divWeights);
      if (json.chartBase64) {
    	  renderChart(json.chartBase64);
      }
    }).catch(function(reason) {
      console.log(reason)
      console.error("Issue with the POST request.")
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
function renderChart(chartBase64) {}
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
  return string.charAt(0).toUpperCase() + string.slice(1);
}
fetchDBsAndPopulateDropdown();
