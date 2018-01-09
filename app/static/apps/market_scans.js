var scanner = new Vue({
    el: '#scanner',
    delimiters: ["<%","%>"],

    data: {
        ask: {
            newName: "",
            newNameChanged: false,
            rawChanged: false,
        },
        scanners: [],
        selected: null,
        loading: false,
        newStationId: 0
    },

    created: function () {
        var vm = this;
        axios.get('/mscans.json')
            .then(function (response) {
                vm.scanners = response.data.list;
                vm.selected = null;
            })
            .catch(function (error) {
                console.log(error);
            });

        new Clipboard('#copy-point', {
            text: function(trigger) {
                return vm.CopyNeed();
            }
        });

        new Clipboard('.copy-item');

    },

    methods: {

        NewNameChanged: function(){
            if(!!this.ask.newName){
                this.ask.newNameChanged = true;
            }
        },

        RawChanged: function(){
            if(this.selected && !!this.selected.raw){
                Vue.set(this.selected, 'rawChanged', true);
            }
        },

        AddStation: function(){
            var vm = this;
            axios.post(
                '/scanner/'+this.selected.Id+'/add_station.json', {station_id: this.newStationId}
            ).then(function (response) {
                vm.selected = response.data.Selected;
            }).catch(function (error) {
                console.log(error);
            });
        },

        DeleteStation: function(stationId){
            var vm = this;
            axios.post(
                '/scanner/'+this.selected.Id+'/delete_station.json', {station_id: stationId}
            ).then(function (response) {
                vm.selected = response.data.Selected;
            }).catch(function (error) {
                console.log(error);
            });
        },

        AddScanner: function(){
            var vm = this;
            axios.post('/mscans.json', {name: this.ask.newName})
                .then(function (response) {
                    vm.scanners = response.data.list;
                    vm.selected = response.data.selected;
                    vm.ask.newName = '';
                    vm.ask.newNameChanged = false;
                })
                .catch(function (error) {
                    console.log(error);
                });

        },

        StartRenameScanner: function(item){
            item.oldName = item.name;
            Vue.set(item, 'editing', true);
        },

        CancelRenameScanner: function(item){
            item.name = item.oldName;
            Vue.set(item, 'editing', false)
        },

        RenameScanner: function(item){
            var vm = this;
            axios.post('/mscans/'+item.id+'/rename.json', {name: item.name})
                .then(function (response) {
                    vm.scanners = response.data.list;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        AskDeleteScanner: function(scannerId){
            if (confirm("Sure?")) {
                var vm = this;
                axios.post('/mscans/'+scannerId+'/delete.json')
                    .then(function (response) {
                        vm.scanners = response.data.list;
                        vm.selected = null;
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        },

        UpdateRawText: function(){
            var vm = this;
            axios.post('/mscans/'+this.selected.id+'.json', {raw: this.selected.raw})
                .then(function (response) {
                    vm.selected = response.data.selected;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        ChangeFitTimes: function(){
            var vm = this;
            axios.post('/scanner/'+this.selected.Id+'.json', {fit_times: parseInt(this.selected.FitTimes)})
                .then(function (response) {
                    vm.selected = response.data.Selected;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        ChangeChar: function(){
            var vm = this;
            axios.post('/scanner/'+this.selected.Id+'.json', {cid: parseInt(this.selected.Cid)})
                .then(function (response) {
                    vm.selected = response.data.Selected;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        UpdateStationId: function(){
            var vm = this;
            axios.post('/scanner/'+this.selected.Id+'.json', {station_id: parseInt(this.selected.StationId)})
                .then(function (response) {
                    vm.selected = response.data.Selected;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        UpdateMarketInfo: function(){
            var vm = this;
            this.loading=true;

            setTimeout(function(){
              axios.post('/scanner/'+vm.selected.Id+'/market_info.json')
                            .then(function (response) {
                                vm.selected = response.data.Selected;
                                vm.loading=false;
                            })
                            .catch(function (error) {
                                console.log(error);
                            });
            }, 1500);


        },

        CopyNeed: function(vm){
            result = "";
            this.selected.Items.forEach(function(el){
                if(el.NeedQty>0){
                    result = result + el.TypeName + ", " + el.NeedQty + "\n";
                }
            });
            return result;
        },

        SetSelected: function(item){
            var vm = this;
            axios.get('/mscans/'+item.id+'.json')
                .then(function (response) {
                    vm.selected = response.data.selected;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        IsSelected: function(item){
            return this.selected != null && this.selected.Id == item.Id;
        }

    },
    filters: {
        number: function (value) {
            return frm.format(value);
        },
        price: function (value) {
            return frmFl.format(value);
        }

     }

})


