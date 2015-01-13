window.onload = function () {
    function scatter(cfg) {
        var spec,
            seasons,
            x,
            y;

        spec = {
            "name": "scatterplot",
            "width": 1200,
            "height": 400,
            "data": [
                {
                    "name": "air/star dates",
                    "url": null
                }
            ],
            "scales": [
                {
                    "name": "y",
                    "type": "linear",
                    "range": "height",
                    "domain": {
                        "data": "air/star dates",
                        "field": "data.stardate"
                    },
                    "zero": false
                },
                {
                    "name": "x",
                    "type": "time",
                    "range": "width",
                    "round": true,
                    "nice": "month",
                    "domain": {
                        "data": "air/star dates",
                        "field": "data.airdate"
                    }
                }
            ],
            "axes": [
                {"type": "x", "scale": "x"},
                {"type": "y", "scale": "y"}
            ],
            "marks": [
                {
                    "type": "symbol",
                    "from": {"data": "air/star dates"},
                    "properties": {
                        "enter": {
                            "x": {"scale": "x", "field": "data.airdate"},
                            "y": {"scale": "y", "field": "data.stardate"},
                            "size": {"value": 50},
                            "stroke": {"value": "black"},
                            "fill": {"value": "steelblue"}
                        },
                        "hover": {
                            "size": {"value": 100},
                            "fill": {"value": "firebrick"}
                        }
                    }
                }
            ]
        };

        cfg = cfg || {};

        spec.data[0].url = "episodes/scatter?x=" + cfg.x + "&y=" + cfg.y;
        if (cfg.seasons) {
            spec.data.url += "&seasons=" + JSON.stringify(cfg.seasons);
        }

        spec.scales[0].domain.field = "data." + cfg.y;
        spec.scales[1].domain.field = "data." + cfg.x;
        spec.marks[0].properties.enter.x.field = "data." + cfg.x;
        spec.marks[0].properties.enter.y.field = "data." + cfg.y;

        return spec;
    }

    function parse(spec) {
        vg.parse.spec(spec, function(chart) {
            var view = chart({el: "#vis"})
                .on("mouseover", function (evt, item) {
                    d3.select("#info")
                        .html(item.datum.data.title);
                })
                .on("mouseout", function (evt, item) {
                    view.update({
                        props: "enter"
                    });
                })
                .update();
        });
    }

    parse(scatter({
        x: "airdate",
        y: "stardate"
    }));
};
