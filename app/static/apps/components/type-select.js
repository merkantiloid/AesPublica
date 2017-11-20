Vue.component('type-select', {
    template: '<input ref="selector" class="type-selector form-control form-control-sm" type="text"/>',

    mounted: function () {
        var vm = this;

        var myAutoComplete = new autoComplete({
            selector: this.$refs.selector,
            minChars: 3,
            delay: 500,
            cache: false,
            source: function(term, suggest){
                axios.get('/search/type?term='+encodeURIComponent(term))
                    .then(function (r) {
                        if(!!r.data){
                            suggest(r.data);
                        }
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            },
            renderItem: function (item, search){
                search = search.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
                var re = new RegExp("(" + search.split(' ').join('|') + ")", "gi");
                return '<div class="autocomplete-suggestion" data-id="'+item.id+'" data-val="'+item.name+'">'+item.name.replace(re, "<b>$1</b>")+'</div>';
            },
            onSelect: function(e, term, item){
                vm.$emit(
                    'type-selected',
                    {
                        id: parseInt(item.getAttribute('data-id')),
                        name: item.getAttribute('data-val')
                    }
                );
            }
        });

    },
})