var calculator = new Vue({
    el: '#calculator',
    delimiters: ["<%","%>"],
    data: {
        title: "Ore Calculator"
    },
    created: function () {
        console.log(this.title)
    }
});