var endpoint = "/overview/convert/projectsdata/";
var labels = [''];
var start_dates = [''];
var end_dates = [''];

$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {
    for (let i in data) {
      labels.push(data[i].name);
      start_dates.push(new Date(data[i].start_date));
      end_dates.push(new Date(data[i].end_date));
    }
    console.log(labels);
    console.log(start_dates);
    console.log(end_dates);
    drawChart();
  },
  error: function (error_data) {
    console.log("error");
    console.log(error_data);
  },
});

function drawChart() {
  var timeFormat = "DD/MM/YYYY";

  // Helper functions 
  /*
  function newDate(days) {
    return moment().add(days, "d").toDate();
  } */

  // Function to parse the dates so ChartJS can read them
  function newDateString(days) {
    return moment().add(days, "d").format(timeFormat);
  }

  /*
This function calculates how many days 
the date from django is form today
*/
  function getDaysFromToday(date) {
    var date1 = new Date(date);
    var date2 = new Date();
    var difference = date1.getTime() - date2.getTime();
    var days = Math.ceil(difference / (1000 * 3600 * 24));
    return Number(days);
  }

  var ctx = document.getElementById("chart1").getContext("2d");

  // Get datasets for the chart
  function getDatasets() {
    console.log('start_dates[0]', start_dates[1]);
    let datasets = [];

    for (let i = 0; i <= labels.length; i++) {
      let days1 = getDaysFromToday(start_dates[i]);
      let days2 = getDaysFromToday(end_dates[i]);

      let set = {
        label: "Ime projekta",
        backgroundColor: "rgba(246,156,85,4)",
        borderColor: "rgba(246,156,85,4)",
        fill: false,
        borderWidth: 15,
        pointRadius: 0,
        data: [
          {
            x: newDateString(days1),
            y: labels[i],
          },
          {
            x: newDateString(days2),
            y: labels[i],
          },
        ],
      };

      datasets.push(set);
    }
    console.log("datasets: ", datasets);
    return datasets;
  }

  var chart_datasets = getDatasets();

  // Chart
  var scatterChart = new Chart(ctx, {
    type: "line",
    data: {
      yLabels: labels,
      datasets: chart_datasets,
    },
    options: {
      legend: {
        display: false,
      },
      scales: {
        xAxes: [
          {
            type: "time",
            time: {
              parser: timeFormat,
            },
          },
        ],
        yAxes: [
          {
            type: "category",
            position: "left",
            display: true,
            scaleLabel: {
              display: true,
              labelString: "Projekti",
            },
            ticks: {
              reverse: true,
            },
          },
        ],
      },
    },
  });
}
