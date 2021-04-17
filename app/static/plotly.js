
/**
 * TODO: render chart
 */
function renderPlotly(plotlyData) {
  function unpack(rows, key) {
    const ind = dummydata_columns.indexOf(key);
    return rows.map(function(row) { return row[ind]; });
  }
  const trace1 = {
    x: unpack(plotlyData, 'x1'),
    y: unpack(plotlyData, 'y1'),
    z: unpack(plotlyData, 'z1'),
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
    x: unpack(plotlyData, 'x2'),
    y: unpack(plotlyData, 'y2'),
    z: unpack(plotlyData, 'z2'),
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
