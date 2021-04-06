let proxIdsSelected = new Set();
let divIdsSelected = new Set();
let selectedDatabaseId = null;
let dbs = [];
const CHECKBOX = "cb";
const TEXTAREA = "ta";
const TIME = "time",
    CLUSTER = "cluster";
let inputState = {
    [TIME]: "",
    [CLUSTER]: ""
};
const PROX = "prox",
    DIV = "div";
let inputWeightState = {
    [PROX]: [],
    [DIV]: []
};
const urlProcess = "process/";
var notyf = new Notyf({
    duration: 10000,
    dismissible: true
});

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
            // document.querySelector(`.attr-item .list-item-cb:disabled[id$='_${taIdInd}']`).removeAttribute("disabled");
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
  /* Request the data and chart */
  const proxIdsAndWeights = [...proxIdsSelected].map(e => [e, parseInt(document.querySelector(`#row_prox_${e} .list-item-weight`).value)]);
  const divIdsAndWeights = [...divIdsSelected].map(e => [e, parseInt(document.querySelector(`#row_div_${e} .list-item-weight`).value)]);
  const time = parseInt(document.querySelector(`.input-time`).value);
    const clusters = parseInt(document.querySelector(`.input-cluster`).value);

    if(!isValideProcessData(time, clusters, proxIdsAndWeights, divIdsAndWeights))
      return;

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
    const proxAttrs = proxWeights.map(e => ({ name: e[0], weight: e[1] }));
    const divAttrs = divWeights.map(e => ({ name: e[0], weight: e[1] }));
    document.querySelector(".process-button-spinner").classList.add("show");
    axios.get('process/', {
            params: { time, clusters, proxAttrs, divAttrs }
    })
    .then(response => {
        let json = response.data
        // Update chart
        let chart = document.querySelector("#chart");
        chart.style.maxHeight = document.querySelector(".data-input-outer-container").clientHeight;
        chart.src = `data:image/png;base64,${json.chart}`;
        // create a reference image from which to take the width and height to calculate maxHeight
        let referenceImg = new Image();
        referenceImg.onload = () => {
            chart.style.maxWidth = document.querySelector(".data-input-outer-container").clientHeight * referenceImg.width / referenceImg.height;
        }
        referenceImg.src = `data:image/png;base64,${json.chart}`;
        document.querySelector(".chart-container").appendChild(chart);
        notyf.success("Processing successful.");
    }).catch(function(reason) {
        console.error("Issue with the Process request.");
        console.error(reason);
        notyf.error("Not able to process the data.");
    }).finally(function() {
        document.querySelector(".process-button-spinner").classList.remove("show");
    });
}

function isValideProcessData(time, clusters, proxIdsAndWeights, divIdsAndWeights) {
  /* Return true if input data is valid */
    let errorSomewhere = false;
    if (proxIdsSelected.size + divIdsSelected.size === 0) {
        document.querySelector(".process-attribute-warning").classList.add("show");
        errorSomewhere = true;
    } else if (document.querySelector(".process-attribute-warning").classList.contains("show")) {
        document.querySelector(".process-attribute-warning").classList.remove("show");
    }
    
    const proxNaN = proxIdsAndWeights.filter(function(pair) { return isNaN(pair[1]); });
    const divNaN = divIdsAndWeights.filter(function(pair) { return isNaN(pair[1]); });
    
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
    return !errorSomewhere;
}
