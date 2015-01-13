window.onload = function () {
    function parse(spec) {
        vg.parse.spec(spec, function(chart) {
            var view = chart({el:"#vis"})
                .on("mouseover", function (evt, item) {
                    console.log(item.datum.data.title);
                })
                .on("mouseout", function (evt, item) {
                    view.update({
                        props: "enter"
                    });
                })
                .update();
        });
    }

    parse("scatter.json");
};
