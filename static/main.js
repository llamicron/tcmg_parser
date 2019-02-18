var app = new Vue({
  el: '#dashboard',
  data: {
    data: {},
    months: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
    // url: 'https://s3.amazonaws.com/tcmg476/http_access_log'
    url: 'https://raw.githubusercontent.com/llamicron/tcmg_parser/master/test_http_access_log'
  },
  methods: {
    get_data() {
      const Http = new XMLHttpRequest();
      Http.open("GET", '/data');
      Http.send();
      Http.onreadystatechange = (e) => {
        this.data = JSON.parse(Http.responseText);
      }
    },

    selectUrl() {
      x = new XMLHttpRequest();
      x.open('POST', '/select-log', async=true);
      x.send(this.url)
      setTimeout(() => {
        this.get_data();
      }, 1000);
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
      this.statusCodesChart = new Chart(document.getElementById("status-codes-chart"), {
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
    },

    renderFileCountChart() {
      var labels = Object.keys(this.data.files).sort((a, b) => { return this.data.files[b] - this.data.files[a] }).slice(0, 10)
      var amounts = []
      labels.forEach(label => {
        amounts.push(this.data.files[label])
      });
      new Chart(document.getElementById("file-count-chart"), {
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
    },

    renderDatesChart() {
      dates = this.datesByMonth()
      el = document.getElementById('dates-chart')
      new Chart(document.getElementById("dates-chart"), {
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
    }
  },
  created() {
    this.get_data();
  },
  computed: {
    totalRequests: function() {
      sum = 0
      Object.values(this.data.status_codes).forEach(amount => {
        sum += parseInt(amount)
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
