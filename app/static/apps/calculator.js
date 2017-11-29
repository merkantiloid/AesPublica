function citadelByID(id){
    return gStatic.citadels.find(function(e){return e.id==id});
}

function recordById(records, id){
    return records.find(function(e){return e.id==id});
}

function r4(n){
    return Math.round( n * 10000 )/10000;
}

function bestRig(meta,ids){
    var bestId = -1;
    ids.forEach(function(id){
        if( gStatic.repr_rigs_hash[id]['metas'].indexOf(meta)>-1 && gStatic.repr_rigs_hash[id].value > gStatic.repr_rigs_hash[bestId].value ){
            bestId = id;
        }
    })
    return gStatic.repr_rigs_hash[bestId];
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
            store_items_text: '',
            store_items: [],
            ore_settings: [],
        },
        static: gStatic,
        rigs: [],
        kOre: 0,
        kIce: 0,
        kScrap: 0,
        newItem: {
            type_id: null,
            type_name: null,
            me: 10,
            te: 20,
            qty: 1,
        },
        newStoreItem: {
            type_id: null,
            type_name: null,
            qty: 1,
        },
        buildItemsTextChanged: false,
        storeItemsTextChanged: false,
        oreSettingsChanged: false,
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
            this.calc.settings.rig2_id = -1;
            this.calc.settings.rig3_id = -1;
            this.rigs = gStatic.repr_rigs[ citadelByID(this.calc.settings.citadel_id).rig_size ];
            this.recalcPercent(event);
            this.saveSettings();
        },

        changeNotCitadel: function() {
            this.recalcPercent(event);
            this.saveSettings();
        },

        recalcPercent: function(){
            var baseOre = bestRig('ore',[this.calc.settings.rig1_id,this.calc.settings.rig2_id,this.calc.settings.rig3_id]),
                baseIce = bestRig('ice',[this.calc.settings.rig1_id,this.calc.settings.rig2_id,this.calc.settings.rig3_id]),
                spaceOre = baseOre[this.calc.settings.space],
                spaceIce = baseIce[this.calc.settings.space],

                implant = 1+recordById(gStatic.repr_implants, this.calc.settings.implant_id).value/100,

                char = recordById(this.calc.settings.characters, this.calc.settings.esi_char_id),
                skill1 = char.skills[3385],
                skill2 = char.skills[3389],
                skillM = char.skills[12196];

            this.kOre  = r4( 100 * baseOre.value * (1+2*5/100.0) * (1+3*skill1/100.0) * (1+2*skill2/100.0) * spaceOre * implant);
            this.kIce  = r4( 100 * baseIce.value * (1+2*5/100.0) * (1+3*skill1/100.0) * (1+2*skill2/100.0) * spaceIce * implant);
            this.kScrap  = r4( 100 * 0.5 * (1+2*skillM/100.0) );
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

        TypeStorageSelected: function(payload){
            this.newStoreItem.type_id = payload.id;
            this.newStoreItem.type_name = payload.name;
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
            $('.build_list input.type-selector').val(null);
            this.buildItemsTextChanged = true;
        },


        AddStoreItem: function(){
            if(this.calc.store_items_text == null){
                this.calc.store_items_text = "";
            }
            if(this.calc.store_items_text != null && this.calc.store_items_text != ''){
                this.calc.store_items_text = this.calc.store_items_text + "\n";
            }

            this.calc.store_items_text = this.calc.store_items_text +
                                         this.newStoreItem.type_name + "\t" +
                                         this.newStoreItem.qty;
            this.newStoreItem.type_id = null;
            this.newStoreItem.type_name = null;
            $('.storage input.type-selector').val(null);
            this.storeItemsTextChanged = true;
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

        UpdateStoreItemsText: function(){
            var vm = this;
            axios.post(
                '/calc/store_items_text',
                {text: vm.calc.store_items_text}
            ).then(function (response) {
                vm.calc.store_items = response.data.store_items;
                vm.calc.minerals = response.data.minerals;
                vm.storeItemsTextChanged = false;
            }).catch(function (error) {
                console.log(error);
            });
        },

        TextChanged: function(){
            this.buildItemsTextChanged = true;
        },

        StoreTextChanged: function(){
            this.storeItemsTextChanged = true;
        },

        IURL: function(type_id){
            return "https://imageserver.eveonline.com/Type/"+type_id+"_32.png"
        },

        SetOres: function(selector){
            $(selector).prop('checked', true);
            this.TouchOreSettings();
        },

        ResetOres: function(selector){
            $(selector).prop('checked', false);
            this.TouchOreSettings();
        },

        OreClasses: function(ore){
            var result = 'ore-input';
            if(ore.compressed_id == null){
                result = result + ' compressed'
            }else{
                result = result + ' common'
            }

            if(ore.compressed_id == null && ore.ore_type == 1){
                result = result + ' simple'
            }

            return result;
        },

        TouchOreSettings: function(){
            var values = $('.ore-input:checked').map(function(i,x){ return x.value }).toArray();
            this.calc.ore_settings = values;
            this.oreSettingsChanged = true;
        },

        SaveOreSettings: function(){
            var vm = this,
                values = $('.ore-input:checked').map(function(i,x){ return x.value }).toArray();
            axios.post(
                '/calc/save_ore_settings',
                {text: values.join(',')}
            ).then(function (response) {
                vm.oreSettingsChanged = false;
                vm.calc.ore_settings = values;
            }).catch(function (error) {
                console.log(error);
            });
        },

        IsOreChecked: function(id){
            return this.calc.ore_settings.indexOf(id.toString()) > -1;
        },

        CalcOres: function(){
            var vm = this;
            console.log('CalcOres');
            axios.get('/calc/result').then(function (response) {
                console.log(response);
            }).catch(function (error) {
                console.log(error);
            });
        },

    }

});