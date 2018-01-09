var scanner = new Vue({
    el: '#scanner',

    data: {
        ask: {Id: null, newName: "", Func: null},
        scanners: [],
        selected: null,
        loading: false,
        newStationId: 0
    },

    created: function () {
        var vm = this;
        axios.get('/mscans.json')
            .then(function (response) {
                vm.scanners = response.data.List;
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

        AskScannerName: function(){
            this.ask.Func = this.AddScanner;
            this.ask.newName = "New Fit on Market";
        },
        AddScanner: function(){
            $('#askStringModal').modal('hide');
            var vm = this;
            axios.post('/scanners.json', {name: this.ask.newName})
                .then(function (response) {
                    vm.scanners = response.data.List;
                    vm.selected = response.data.Selected;
                })
                .catch(function (error) {
                    console.log(error);
                });

        },

        AskRenameScannerName: function(item){
            this.ask.Func = this.RenameScanner;
            this.ask.newName = item.Name;
            this.ask.Id = item.Id;
        },
        RenameScanner: function(){
            $('#askStringModal').modal('hide');
            var vm = this;
            axios.post('/scanner/'+this.ask.Id+'/rename.json', {name: this.ask.newName})
                .then(function (response) {
                    vm.scanners = response.data.List;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        AskDeleteScanner: function(scannerId){
            if (confirm("Sure?")) {
                var vm = this;
                axios.post('/scanner/'+scannerId+'/delete.json')
                    .then(function (response) {
                        vm.scanners = response.data.List;
                        vm.selected = null;
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        },

        UpdateRawText: function(){
            var vm = this;
            axios.post('/scanner/'+this.selected.Id+'.json', {raw: this.selected.Raw})
                .then(function (response) {
                    vm.selected = response.data.Selected;
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
            axios.get('/scanner/'+item.Id+'.json')
                .then(function (response) {
                    vm.selected = response.data;
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


