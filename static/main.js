var app = new Vue({
  el: '#dashboard',
  data: {
    data: {}
  },
  methods: {
    async get_data() {
      const Http = new XMLHttpRequest();
      Http.open("GET", '/data');
      Http.send();
      Http.onreadystatechange = (e) => {
        this.data = Http.responseText;
      }
    }
  },
  created() {
    this.get_data();
  }
})
