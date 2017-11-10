function citadelByID(id){
    return gStatic.citadels.find(function(e){return e.id==id});
}

function recordById(records, id){
    return records.find(function(e){return e.id==id});
}

function r4(n){
    return Math.round( n * 10000 )/10000;
}

var calculator = new Vue({
    el: '#calculator',
    delimiters: ["<%","%>"],
    data: {
        calc: {},
        static: gStatic,
        rigs: [],
        kOreLow: 0,
        kOreHi: 0,
        kScrap: 0,
    },

    created: function () {
        var vm = this;
        axios.get('/calc/data.json')
            .then(function (response) {
                vm.calc = response.data;
                vm.rigs = gStatic.repr_rigs[ citadelByID(vm.calc.citadel_id).rig_size ];
                vm.recalcPercent();
            })
            .catch(function (error) {
                console.log(error);
            });
    },

    methods: {
      changeCitadel: function() {
          this.calc.rig1_id = -1;
          this.rigs = gStatic.repr_rigs[ citadelByID(this.calc.citadel_id).rig_size ];
          this.recalcPercent(event);
          this.saveSettings();
      },

      changeNotCitadel: function() {
          this.recalcPercent(event);
          this.saveSettings();
      },

      recalcPercent: function(){
          var base = gStatic.repr_rigs_hash[this.calc.rig1_id].value,
              char = recordById(this.calc.characters, this.calc.esi_char_id),
              space = gStatic.repr_rigs_hash[this.calc.rig1_id][this.calc.space],
              implant = 1+recordById(gStatic.repr_implants, this.calc.implant_id).value/100,
              skill1 = char.skills[3385],
              skill2 = char.skills[3389],
              skillM = char.skills[12196];
          this.kOreLow = r4( 100 * base * (1+2*4/100.0) * (1+3*skill1/100.0) * (1+2*skill2/100.0) * space * implant);
          this.kOreHi  = r4( 100 * base * (1+2*5/100.0) * (1+3*skill1/100.0) * (1+2*skill2/100.0) * space * implant);
          this.kScrap  = r4( 100 * base * (1+2*skillM/100.0)  * space * implant);
      },

      saveSettings: function(){
        var vm = this;
        axios.post(
            '/calc/save_settings',
            {
                "space":        vm.calc.space,
                "citadel_id":   vm.calc.citadel_id,
                "esi_char_id":  vm.calc.esi_char_id,
                "implant_id":   vm.calc.implant_id,
                "rig1_id":      vm.calc.rig1_id,
            }
        ).then(function (response) {

        }).catch(function (error) {
            console.log(error);
        });
      }

    }

});