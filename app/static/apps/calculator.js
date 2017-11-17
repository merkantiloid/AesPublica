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
        calc: {
            settings: {},
            build_items_text: '',
            build_items: [],
            minerals: [],
        },
        static: gStatic,
        rigs: [],
        kOreLow: 0,
        kOreHi: 0,
        kScrap: 0,
        newItem: {
            type_id: null,
            type_name: null,
            me: 10,
            te: 20,
            qty: 1,
        },
        buildItemsTextChanged: false
    },

    created: function () {
        var vm = this;
        axios.get('/calc/data.json')
            .then(function (response) {
                vm.calc = response.data;
                vm.rigs = gStatic.repr_rigs[ citadelByID(vm.calc.settings.citadel_id).rig_size ];
                vm.recalcPercent();
            })
            .catch(function (error) {
                console.log(error);
            });
    },

    methods: {
        changeCitadel: function() {
            this.calc.settings.rig1_id = -1;
            this.rigs = gStatic.repr_rigs[ citadelByID(this.calc.settings.citadel_id).rig_size ];
            this.recalcPercent(event);
            this.saveSettings();
        },

        changeNotCitadel: function() {
            this.recalcPercent(event);
            this.saveSettings();
        },

        recalcPercent: function(){
            var base = gStatic.repr_rigs_hash[this.calc.settings.rig1_id].value,
                char = recordById(this.calc.settings.characters, this.calc.settings.esi_char_id),
                space = gStatic.repr_rigs_hash[this.calc.settings.rig1_id][this.calc.settings.space],
                implant = 1+recordById(gStatic.repr_implants, this.calc.settings.implant_id).value/100,
                skill1 = char.skills[3385],
                skill2 = char.skills[3389],
                skillM = char.skills[12196];
            this.kOreLow = r4( 100 * base * (1+2*4/100.0) * (1+3*skill1/100.0) * (1+2*skill2/100.0) * space * implant);
            this.kOreHi  = r4( 100 * base * (1+2*5/100.0) * (1+3*skill1/100.0) * (1+2*skill2/100.0) * space * implant);
            this.kScrap  = r4( 100 * base * (1+2*skillM/100.0) * implant);
        },

        saveSettings: function(){
            var vm = this;
            axios.post(
                '/calc/save_settings',
                vm.calc.settings
            ).then(function (response) {

            }).catch(function (error) {
                console.log(error);
            });
        },

        TypeSelected: function(payload){
            this.newItem.type_id = payload.id;
            this.newItem.type_name = payload.name;
        },

        AddBuildItem: function(){
            if(this.calc.build_items_text == null){
                this.calc.build_items_text = "";
            }
            if(this.calc.build_items_text != null && this.calc.build_items_text != ''){
                this.calc.build_items_text = this.calc.build_items_text + "\n";
            }

            this.calc.build_items_text = this.calc.build_items_text +
                                         this.newItem.type_name + "\t" +
                                         this.newItem.qty + "\t"+
                                         "ME" + this.newItem.me + "\t"+
                                         "TE" + this.newItem.te;
            this.newItem.type_id = null;
            this.newItem.type_name = null;
            $('input.type-selector').val(null);
            this.buildItemsTextChanged = true;
        },

        UpdateBuildItemsText: function(){
            var vm = this;
            axios.post(
                '/calc/build_items_text',
                {text: vm.calc.build_items_text}
            ).then(function (response) {
                vm.calc.build_items = response.data.build_items;
                vm.calc.minerals = response.data.minerals;
                vm.buildItemsTextChanged = false;
            }).catch(function (error) {
                console.log(error);
            });
        },

        TextChanged: function(){
            this.buildItemsTextChanged = true;
        },

        IURL: function(type_id){
            return "https://imageserver.eveonline.com/Type/"+type_id+"_32.png"
        }

    }

});