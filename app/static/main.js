let proxIdsSelected = new Set();
let divIdsSelected = new Set();
let selectedDatabaseId = null;
const CHECKBOX = "cb"; const TEXTAREA = "ta";
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
      // don't need [id^='cb_'] because all checkbox ids start with that
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
  fetchAndDisplayCardsAttrs();
}
function fetchAndDisplayCardsAttrs() {
  // TODO: fetch attributes
  // fetch.then(
  // attrList = arr;
  document.querySelectorAll(".card .attr-item").forEach(e => e.parentNode.removeChild(e));
  document.querySelector("#card-prox").innerHTML += genListItemsForType(attrList, true);
  document.querySelector("#card-div").innerHTML += genListItemsForType(attrList, false);
  // );
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
  // might not need checkboxId
  const checkboxId = `cb_${type}_${id}`;
  const textAreaId = `ta_${type}_${id}`;
  const warningId = `w_${type}_${id}`;
  // Return string of element
  return (`
    <div id="${rowId}" class="list-item attr-item">
      <!-- checkbox & attribute -->
      <div class="list-item-cbattr">
        <label class="list-item-cbattr-label">
          <input id="${checkboxId}" class="list-item-cb" type="checkbox" onclick="handleAttrClick(${isProx})(this)">
          <span><strong style="font-size:1rem;">${attrProperCase}</strong></span>
        </label>
      </div>
      <!-- input -- if you wanted to accept decimal points event.charCode == 46-->
      <input
        id="${textAreaId}" class="list-item-weight" type="text" placeholder="Weight" disabled=true
        onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"
      />
      <!-- warning svg -->
      <i id="${warningId}" class="fas fa-exclamation-triangle list-item-warning"></i>
    </div>
  `);
}
function process() {
  if (proxIdsSelected.size + divIdsSelected.size === 0) {
    document.querySelector(".process-warning").classList.add("show");
  } else if (document.querySelector(".process-warning").classList.contains("show")) {
    document.querySelector(".process-warning").classList.remove("show");
  }
  const proxIdsAndWeights = [...proxIdsSelected].map(e => [e, parseInt(document.querySelector(`#row_prox_${e} .list-item-weight`).value)]);
  const divIdsAndWeights = [...divIdsSelected].map(e => [e, parseInt(document.querySelector(`#row_div_${e} .list-item-weight`).value)]);
  const proxNaN = proxIdsAndWeights.filter(function(pair) { return isNaN(pair[1]); });
  const divNaN = divIdsAndWeights.filter(function(pair) { return isNaN(pair[1]); });
  document.querySelectorAll(".attr-item .list-item-warning").forEach(function(e) { e.classList.remove("show"); });
  if (proxNaN.length + divNaN.length !== 0) {
    proxNaN.forEach(function(pair) {
      document.querySelector(`#row_prox_${pair[0]} .list-item-warning`).classList.add("show");
    });
    divNaN.forEach(function(pair) {
      document.querySelector(`#row_div_${pair[0]} .list-item-warning`).classList.add("show");
    });
  } else {
    const proxWeights = proxIdsAndWeights.map(function(pair) { let p = [...pair]; p[0] = attrList[p[0]]; return p; });
    const divWeights = divIdsAndWeights.map(function(pair) { let p = [...pair]; p[0] = attrList[p[0]]; return p; });
    console.log(proxWeights, divWeights);
    // TODO: Make a POST request
    // TODO: Create a summary from the request response
    // fetch(`url`, {
    // 	method: 'POST',
    // 	headers: {
    // 		'Accept': 'application/json',
    // 		'Content-Type': 'application/json'
    // 	},
    // 	body: JSON.stringify(data)
    // }).then((response) => {
    // 	return response.json;
    // }).then((json) => {
    //	// createSummary(json.data);
      createSummary(undefined, proxWeights, divWeights);
    //	// renderChart(json.chartBase64);
    // });
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