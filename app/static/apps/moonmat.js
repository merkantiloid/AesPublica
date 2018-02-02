var scanner = new Vue({
    el: '#moonmat',
    delimiters: ["<%","%>"],

    data: {
        ask: {
            rig_id: 0,
            rawChanged: false,
        },
        settings: {},
        rigs: [],
        spaces: [],
        items: [],
        materials: [],
        totals: [],
        raw: null,
    },

    created: function () {
        var vm = this;
        axios.get('/moonmat/data.json')
            .then(function (response) {
                vm.spaces = response.data.spaces;
                vm.settings = response.data.settings;
                vm.rigs = response.data.rigs;
                vm.raw = response.data.raw;
                vm.items = response.data.items;
                vm.materials = response.data.materials;
                vm.totals = response.data.totals;
            })
            .catch(function (error) {
                console.log(error);
            });

        new Clipboard('#copy-point', {
            text: function(trigger) {
                return vm.CopyTotals();
            }
        });
    },

    methods: {

        OnSettingsChange: function(){
        },

        AddRig: function(){
            var vm = this;
            axios.post('/moonmat/rigs.json', {rig_id: this.ask.rig_id})
                .then(function (response) {
                    vm.materials = response.data.materials;
                    vm.totals = response.data.totals;
                    vm.settings = response.data.settings;
                    vm.ask.rig_id=0;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        DeleteRig: function(rig_id){
            var vm = this;
            axios.delete('/moonmat/rigs/'+rig_id+'.json')
                .then(function (response) {
                    vm.materials = response.data.materials;
                    vm.totals = response.data.totals;
                    vm.settings = response.data.settings;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        RawChanged: function(){
            if(!!this.raw){
                this.ask.rawChanged = true;
            }
        },

        UpdateRawText: function(){
            var vm = this;
            axios.post('/moonmat.json', {raw: this.raw})
                .then(function (response) {
                    vm.materials = response.data.materials;
                    vm.totals = response.data.totals;
                    vm.ask.rawChanged = false;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        CopyTotals: function(){
            result = "";
            this.totals.forEach(function(el){
                result = result + el.type.name + ", " + el.qty + "\n";
            });
            return result;
        },


    },
})


