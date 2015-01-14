$(function () {
    "use strict";

    function barchart(cfg) {
        var spec,
            height = cfg.height || 400,
            width = cfg.width || 8000,
            sort = cfg.sort || false;

        spec = {
            name: "barchart",
            width: width,
            height: height,
            data: [
                {
                    name: "table",
                    url: "writers/count?sort=" + sort
                }
            ],
            scales: [
                {
                    name: "y",
                    type: "linear",
                    range: "height",
                    domain: {
                        data: "table",
                        field: "data." + cfg.value
                    }
                },
                {
                    name: "x",
                    type: "ordinal",
                    range: "width",
                    domain: {
                        data: "table",
                        field: "data." + cfg.label
                    }
                }
            ],
            axes: [
                {
                    type: "x",
                    scale: "x",
                    values: []
                },
                {
                    type: "y",
                    scale: "y",
                    grid: false
                }
            ],
            marks: [
                {
                    type: "rect",
                    from: {data: "table"},
                    properties: {
                        enter: {
                            x: {scale: "x", field: "data." + cfg.label, offset: -1},
                            width: {scale: "x", band: true, offset: -1},
                            y: {scale: "y", field: "data." + cfg.value},
                            y2: {scale: "y", value: 0},
                            fill: {value: "steelblue"}
                        },
                        update: {
                            fill: {value: "steelblue"}
                        },
                        hover: {
                            fill: {value: "firebrick"}
                        }
                    }
                },
                {
                    type: "text",
                    from: {data: "table"},
                    properties: {
                        enter: {
                            x: {scale: "x", field: "data." + cfg.label},
                            y: {value: height + 5},
                            angle: {value: 45},
                            fill: {value: "black"},
                            text: {field: "data." + cfg.label},
                            font: {value: "Helvetica Neue"},
                            fontSize: {value: 15}
                        }
                    }
                }
            ]
        };

        return spec;
    }

    if (false) {
        $.getJSON("writers/count", function (writers) {
            $("#vis").barChart({
                label: tangelo.accessor({field: "name"}),
                value: tangelo.accessor({field: "count"}),
                data: writers,
                width: 8000,
                height: 400
            });
        });
    }

    function parse(spec) {
        vg.parse.spec(spec, function (chart) {
            chart({el: "#vis"}).update();
        });
    }

    parse(barchart({
        label: "name",
        value: "count",
        width: 4000,
        sort: true
    }));
});
