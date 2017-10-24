function citadelByID(id){
    return gStatic.citadels.find(function(e){return e.id==id});
}

var calculator = new Vue({
    el: '#calculator',
    delimiters: ["<%","%>"],
    data: {
        calc: {},
        static: gStatic,
        rigs: []
    },

    created: function () {
        var vm = this;
        axios.get('/calc/data.json')
            .then(function (response) {
                vm.calc = response.data;
                vm.rigs = gStatic.repr_rigs[ citadelByID(vm.calc.citadel_id).rig_size ];
            })
            .catch(function (error) {
                console.log(error);
            });
    },

    methods: {
      changeCitadel: function(event) {
          this.calc.rig1_id = -1;
          this.calc.rig2_id = -1;
          this.calc.rig3_id = -1;
          this.rigs = gStatic.repr_rigs[ citadelByID(this.calc.citadel_id).rig_size ];

      }
    }

});