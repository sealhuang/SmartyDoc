// call "jupyter nbconvert" and open generated html file in new tab

define([
    'base/js/namespace',
    'jquery',
    'base/js/events',
    'base/js/utils'
], function(
    IPython,
    $,
    events,
    utils
) {
    "use strict";

    var nbconvert_options = '--execute --to html --template=./templates/report_sample.tpl --output tmp.html';
    var to_pdf = true;
    var pdf_command = ' ';
    var open_tab = true;
    var toc_level = 1;
    var include_foreword = ' ';
    var include_article_summary = ' ';

    /**
     * Get option from config
     */
    var initialize = function () {
        var config = IPython.notebook.config;
        if (config.data.hasOwnProperty('printview2.nbconvert_options') ) {
            nbconvert_options = config.data.printview_nbconvert_options;
        }
	if (config.data.hasOwnProperty('printview2.to_pdf') ) {
	    if (typeof(config.data.printview2.to_pdf) === "boolean") {
		to_pdf = config.data.printview2.to_pdf;
            }
        }
        if (config.data.hasOwnProperty('printview2.open_tab') ) {
            if (typeof(config.data.printview2.open_tab) === "boolean") {
                open_tab = config.data.printview_open_tab;
            }
        }
        if (config.data.hasOwnProperty('printview2.has_foreword') ) {
            if (typeof(config.data.printview2.has_foreword) === "boolean") {
                if (config.data.printview2.has_foreword === true) {
                    include_foreword = ' --include_foreword ';
                }
            }
        }
        if (config.data.hasOwnProperty('printview2.toc_level') ) {
            toc_level = config.data.printview2.toc_level;
        }
        if (config.data.hasOwnProperty('printview2.include_article_summary') ) {
            if (config.data.printview2.include_article_summary === 'none') {
                include_article_summary = ' ';
	    } else {
		include_article_summary = ' --include_article_summary ' + config.data.printview2.include_article_summary;
            }
        }
    };

    /**
     * Call nbconvert using the current notebook server profile
     *
     */
    var callNbconvert = function () {
        events.off('notebook_saved.Notebook');
        var kernel = IPython.notebook.kernel;
        var name = IPython.notebook.notebook_name;
        var out_html = utils.splitext(name)[0] + '.html';
        var out_pdf = utils.splitext(name)[0] + '.pdf';
        var command = 'import os; os.system(\'jupyter nbconvert ' + nbconvert_options + ' \"' + name + '\"\');' + 'os.system(\'trans2std --in tmp.html --out_file ' + out_html + ' --toc_level ' + toc_level + include_foreword + include_article_summary + '\');' + 'os.system(\'rm tmp.html\');'
	if (to_pdf === true) {
            pdf_command = 'weasyprint ' + out_html + ' ' + out_pdf;
	    command = command + 'os.system(\'' + pdf_command + '\');';
            var out_file = out_pdf;
	} else {
	    var out_file = out_html;
	}

        function callback() {
            if (open_tab === true) window.open(out_file, '_blank');
        }

        kernel.execute(command, { shell: { reply : callback } });
        $('#doPrintView').blur();
    };

    var nbconvertPrintView = function () {
        events.on('notebook_saved.Notebook',callNbconvert);
        IPython.notebook.save_notebook(false);
    };

    var load_ipython_extension = function() {
        $(IPython.toolbar.add_buttons_group([
            IPython.keyboard_manager.actions.register ({
                help   : 'Create static print view',
                icon   : 'fa-print',
                handler: nbconvertPrintView
            }, 'create-static-printview',  'printview'),
        ])).find('.btn').attr('id', 'doPrintView');
        return IPython.notebook.config.loaded.then(initialize);
    };

    return {
        load_ipython_extension : load_ipython_extension
    };
});
