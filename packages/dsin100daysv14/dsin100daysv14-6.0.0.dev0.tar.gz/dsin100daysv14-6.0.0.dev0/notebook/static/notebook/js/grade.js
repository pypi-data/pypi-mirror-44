// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events',
], function(
    $,
    Jupyter,
    events,
) {
    "use strict";
    // NOTE: all the functions should be idempotent, i.e on multiple load of same
    // function should have same behaviour

    function add_submit_button() {
        var ncells = Jupyter.notebook.ncells();
        var cells = Jupyter.notebook.get_cells();
        for (var i=0; i<cells.length; i++) {
            var cell = cells[i];
            console.log(cell);
            if (cell.metadata.tags && cell.metadata.tags.includes('grade')) {

            }
        }
    }

    var add_submit_button = function () {
        Jupyter.notebook.get_cells().forEach(function(cell) {
            if (cell.metadata.tags && cell.metadata.tags.includes('grade')) {
                var code = 'var index = $(this).parent().parent().parent().index(); console.log(index); var cell = Jupyter.notebook.get_cell(index); cell.execute();'
                cell.element.find("div.inner_cell")
                    .prepend(`<button onclick='`+code+`' style="width: 100%">Submit</button>`);
                cell.element.find("div.inner_cell").find("div").hide();
                events.on("execute.CodeCell", function (e, d) {
                    d.cell.element.find('button').text('Submitting..');
                });
                events.on("finished_execute.CodeCell", function (e, d) {
                    setTimeout(function () {
                        d.cell.element.find('button').text('Submit');
                    }, 1000);
                });
            }
        })
    };

    function load_functions() {
        add_submit_button();
    }

    var load_extension = function() {
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
            load_functions();
        }
        events.on("notebook_loaded.Notebook", load_functions);
    };

    return {
        load_extension : load_extension
    };
});
