var endpoint = "/overview/avail_data/";
var nums_of_workers = [];
var dates = [];

$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {
    for (let i in data) {
      nums_of_workers.push(data[i].num_of_workers);
      dates.push(new Date(data[i].date));
    }

    drawChart1();
  },
  error: function (error_data) {
    console.log("error");
    console.log(error_data);
  },
});

function drawChart1() {
  var timeFormat = "DD/MM/YYYY";

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

  // Get datasets for the chart
  function getDataset() {
    var dataset = [];
    let prev_num = 0;

    for (let i = 0; i <= dates.length; i++) {
      // Check if num of workers changed
      if (nums_of_workers[i] != prev_num) {
        // Have to calculate how many days from today is given date
        // To feed it to momentjs
        let days = getDaysFromToday(dates[i]);

        var set = {
          x: newDateString(days),
          y: nums_of_workers[i],
        };
        dataset.push(set);
        prev_num = nums_of_workers[i];
      }
    }
    console.log(dataset);
    return dataset;
  }

  function get_labels() {
    for (let i in dates) {
      var list1 = [];
      let temp = i.toString();
      list1.push(temp);
    }
    return list1;
  }
  var ctx2 = document.getElementById("chart2").getContext("2d");
  // Chart
  var myLineChart = new Chart(ctx2, {
    type: "line",
    data: {
      datasets: [
        {
          label: "Število prostih delavcev",
          backgroundColor: "#d85408",
          borderColor: "#d85408",
          steppedLine: "before",
          fill: false,
          data: getDataset(),
        },
      ],
    },
    options: {
      scales: {
        xAxes: [
          {
            type: "time",
            time: {
              parser: timeFormat,
            },
          },
        ],
        /*
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ], */
      },
      responsive: true,
      title: {
        display: false,
      },
    },
  });
}
