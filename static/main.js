var app = new Vue({
  el: '#dashboard',
  data: {
    data: {},
    months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    loading: false,
    charts: [],
    // url: 'https://s3.amazonaws.com/tcmg476/http_access_log',
    url: 'https://raw.githubusercontent.com/llamicron/tcmg_parser/master/test_http_access_log',
  },
  methods: {
    parse(url='') {
      // Post a url to the server and loads the data it parses from that url
      const Http = new XMLHttpRequest();
      Http.open("POST", '/parse');
      Http.send(this.url);
      this.loading = true
      Http.onreadystatechange = (e) => {
        this.destroyCharts();
        this.data = JSON.parse(Http.responseText);
        this.loading = false
      }
    },

    datesByMonth() {
      // This is bad and i hate everything
      dates = this.data.dates
      keys = Object.keys(dates)
      newDates = {}
      this.months.forEach(month => {
        monthKeys = keys.filter(x => x.slice(3, 6) == month)
        monthKeys.forEach(monthKey => {
          if (!newDates[month]) {
            newDates[month] = 0;
          }
          newDates[month] += dates[monthKey];
        });
      });
      return this.months.map(m => newDates[m]);
    },

    renderCharts() {
      this.renderStatusCodesChart();
      this.renderFileCountChart();
      this.renderDatesChart();
    },

    renderStatusCodesChart() {
      data = [
        this.data['status_codes']['2xx'],
        this.data['status_codes']['3xx'],
        this.data['status_codes']['4xx'],
        this.data['status_codes']['5xx'],
      ]
      chart = new Chart(document.getElementById("status-codes-chart"), {
        type: 'doughnut',
        data: {
          labels: ['2xx', '3xx', '4xx', '5xx'],
          datasets: [
            {
              label: 'Amount',
              backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
              data: data
            }
          ]
        },
        options: {
          title: {
            display: true,
            text: 'Amount of requests per status code'
          }
        }
      });
      this.charts.push(chart)
    },

    renderFileCountChart() {
      var labels = Object.keys(this.data.files).sort((a, b) => { return this.data.files[b] - this.data.files[a] }).slice(0, 10)
      var amounts = []
      labels.forEach(label => {
        amounts.push(this.data.files[label])
      });
      chart = new Chart(document.getElementById("file-count-chart"), {
        type: 'horizontalBar',
        data: {
          labels: labels,
          datasets: [
            {
              label: "Request Count",
              backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
              data: amounts
            }
          ]
        },
        options: {
          legend: { display: false },
          title: {
            display: true,
            text: 'Most Requested Files'
          }
        }
      });
      this.charts.push(chart)
    },

    renderDatesChart() {
      dates = this.datesByMonth()
      el = document.getElementById('dates-chart')
      chart = new Chart(document.getElementById("dates-chart"), {
        type: 'line',
        data: {
          labels: this.months,
          datasets: [
            {
              data: Object.values(dates),
              label: "Requests",
              borderColor: "#3e95cd",
              fill: false
            }
          ]
        },
        options: {
          title: {
            display: true,
            text: 'Requests per month'
          }
        }
      });
      this.charts.push(chart)
    },

    destroyCharts() {
      this.charts.forEach(chart => {
        chart.destroy();
      });
      this.charts = []
    }
  },
  created() {
    this.parse();
  },
  computed: {
    totalRequests: function() {
      sum = 0
      Object.keys(this.data.status_codes).forEach(key => {
        sum += this.data.status_codes[key]
      });
      return sum
    },
    badRequests: function() {
      return parseInt(this.data['status_codes']['3xx'] + this.data['status_codes']['4xx'] + this.data['status_codes']['5xx'])
    },
    goodRequests: function() {
      return parseInt(this.data['status_codes']['2xx'])
    }
  },
  watch: {
    data: {
      deep: true,
      handler() {
        this.renderCharts();
      }
    }
  }
})
