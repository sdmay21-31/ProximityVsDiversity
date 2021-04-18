let proxIdsSelected = new Set();
let divIdsSelected = new Set();
let selectedDatabaseId = null;
let dbs = [];
const CHECKBOX = "cb",
  TEXTAREA = "ta";
const TIME = "time",
  CLUSTER = "cluster";
let inputTimeState = "";
let inputState = {
  [TIME]: "0",
  [CLUSTER]: "3"
};
const PROX = "prox",
  DIV = "div";
let inputWeightState = {
  [PROX]: [],
  [DIV]: []
};
const INSTRUCTION = "instruction",
  MIN = "min", MAX = "max";
const paramToInputInfo = Object.freeze({
  "clusters": {
    [INSTRUCTION]: "Enter number of clusters between 1 and 20, inclusive",
    [MIN]: 1,
    [MAX]: 20
  },
  "neighborhoodSize": {
    [INSTRUCTION]: "Enter the target neighborhood size",
    [MIN]: 1,
    [MAX]: 20
  },
  "branchingFactor": {
    [INSTRUCTION]: "",
    [MIN]: 0,
    [MAX]: 0
  },
  "threshold": {
    [INSTRUCTION]: "",
    [MIN]: 0,
    [MAX]: 0
  }
});

const urlProcess = "process/";
var notyf = new Notyf({
  duration: 10000,
  dismissible: true
});

setFirstState();

function setFirstState() {
  document.querySelector(".input-time").value = inputState[TIME];
  document.querySelector(".input-cluster").value = inputState[CLUSTER];
}

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
      arr.add(taIdInd);
      textarea.removeAttribute("disabled");
      if (textarea.value === "") {
        if(forProx)
          textarea.value = "1";
        else
          textarea.value = ".1"
        inputWeightState[taId[1]][taId[2]] = "1";
      }
      document.querySelectorAll(`.attr-item .list-item-cb[id$='_${taIdInd}']:not(:checked)`).forEach(function(e) {
        e.setAttribute("disabled", true);
      });
      if (proxIdsSelected.size === 3) {
        document.querySelectorAll("#proximity_attributes .attr-item .list-item-cb:not(:checked)").forEach(function(e) {
          e.setAttribute("disabled", true);
        });
      }
    }
    return 1;
  }
}

function controlInputWeight(event) {
  const [, type, ind] = event.target.id.toLowerCase().split("_");
  const value = event.target.value;
  if (isNaN(value)) {
    event.target.value = inputWeightState[type][ind];
  }
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

function controlDynamicInputs(event) {}

function toggleAlgoDropdown(ddButton) {
  document.querySelector(".algo-dropdown-options").classList.toggle("show");
}

function handleAlgoDropdownSelect(event) {}

function process() {
  /* Request the data and chart */
  const proxIdsAndWeights = [...proxIdsSelected].map(e => [e, parseFloat(document.querySelector(`#row_prox_${e} .list-item-weight`).value)]);
  const divIdsAndWeights = [...divIdsSelected].map(e => [e, parseFloat(document.querySelector(`#row_div_${e} .list-item-weight`).value)]);
  const time = parseInt(document.querySelector(`.input-time`).value);
  const clusters = parseInt(document.querySelector(`.input-cluster`).value);
  if (!isValidProcessData(time, clusters, proxIdsAndWeights, divIdsAndWeights)) return;
  const proxWeights = proxIdsAndWeights.map(function(pair) {
    let p = [...pair];
    p[0] = attrList[p[0]];
    return p;
  });
  const divWeights = divIdsAndWeights.map(function(pair) {
    let p = [...pair];
    p[0] = attrList[p[0]];
    return p;
  });
  document.querySelector(".process-button").setAttribute("disabled", true);
  document.querySelector(".process-button-spinner").classList.add("show");
  let params = simpleQueryString.stringify({
    time, 
    clusters,
    proximity_attributes: proxWeights.map(x => x[0]),
    proximity_weights: proxWeights.map(x => x[1]),
    diversity_attributes: divWeights.map(x => x[0]),
    diversity_weights: divWeights.map(x => x[1])
  });
  axios.get(`process/?${params}`).then(response => {
    let json = response.data
    // Update chart
    let chart = document.querySelector("#chart");
    chart.style.maxHeight = document.querySelector(".data-input-container").clientHeight;
    chart.src = `data:image/png;base64,${json.chart}`;
    // create a reference image from which to take the width and height to calculate maxHeight
    let referenceImg = new Image();
    referenceImg.onload = () => {
      chart.style.maxWidth = document.querySelector(".data-input-container").clientHeight * referenceImg.width / referenceImg.height;
    }
    referenceImg.src = `data:image/png;base64,${json.chart}`;
    notyf.success("Processing successful.");
  }).catch(function(reason) {
    console.error("Issue with the Process request.");
    console.error(reason);
    notyf.error("Not able to process the data.");
  }).finally(function() {
    document.querySelector(".process-button").removeAttribute("disabled");
    document.querySelector(".process-button-spinner").classList.remove("show");
  });
}

function isValidProcessData(time, clusters, proxIdsAndWeights, divIdsAndWeights) {
  /* Return true if input data is valid */
  let errorSomewhere = false;
  if (proxIdsSelected.size + divIdsSelected.size === 0) {
    document.querySelector(".process-attribute-warning").classList.add("show");
    errorSomewhere = true;
  } else if (document.querySelector(".process-attribute-warning").classList.contains("show")) {
    document.querySelector(".process-attribute-warning").classList.remove("show");
  }
  
  document.querySelectorAll(".attr-item .list-item-warning").forEach(function(e) { e.classList.remove("show"); });
  document.querySelector(".input-time").classList.remove("error");
  document.querySelector(".process-time-warning").classList.remove("show");
  document.querySelector(".input-cluster").classList.remove("error");
  document.querySelector(".process-cluster-warning").classList.remove("show");

  return !errorSomewhere;
}

function fakeProcess() {
  let chart = document.querySelector("#chart");
  chart.style.maxHeight = document.querySelector(".data-input-container").clientHeight;
  chart.src = `data:image/png;base64,${imgPath}`;
  let referenceImg = new Image();
  referenceImg.onload = () => {
    chart.style.maxWidth = document.querySelector(".data-input-container").clientHeight * referenceImg.width / referenceImg.height;
  }
  referenceImg.src = `data:image/png;base64,${imgPath}`;
}
