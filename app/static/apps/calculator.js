var calculator = new Vue({
    el: '#calculator',
    delimiters: ["<%","%>"],
    data: {
        calc: {}
    },
    created: function () {
        var vm = this;
        axios.get('/calc/data.json')
            .then(function (response) {
                vm.calc = response.data;
            })
            .catch(function (error) {
                console.log(error);
            });
    }
});