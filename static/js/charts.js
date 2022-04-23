$("#botonFecha").click(function () {
    try {
      dateChart.destroy();
    } catch { }
    var ctx2 = document.getElementById("chartCanvas2").getContext("2d");
    dateChart = new Chart(ctx2, {
      type: 'bar',
      options: {
        responsive: true,
        scales: { yAxes: [{ ticks: { beginAtZero: true } }] }
      }
    });
    crearChart("/reportes/dateChart/"+$("#fechaI").val()+"&"+$("#fechaF").val(), dateChart);
  });
  $("#categorias").change(function () {
    try {
      categoriaChart.destroy();
    } catch { }
    var ctx = document.getElementById("chartCanvas").getContext("2d");
    categoriaChart = new Chart(ctx, {
      type: 'bar',
      options: {
        responsive: true,
        scales: { yAxes: [{ ticks: { beginAtZero: true } }] }
      }
    });

    crearChart("/reportes/stockChart/" + $("#categorias option:selected").val(), categoriaChart);
  });

  function crearChart(link, chart) {
    $.ajax({
      url: link,
      type: "GET",
      dataType: "json",
      success: (jsonResponse) => {

        const title = jsonResponse.title;
        const labels = jsonResponse.data.labels;
        const datasets = jsonResponse.data.datasets;

        // Load new data into the chart
        chart.options.title.text = title;
        chart.options.title.display = true;
        chart.data.labels = labels;
        datasets.forEach(dataset => {
          chart.data.datasets.push(dataset);
        });
        chart.update();
      },
      error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
    });
  };