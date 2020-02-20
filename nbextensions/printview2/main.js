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
    var add_heading_number = ' ';
    var include_foreword = ' ';
    var include_article_summary = ' ';

    /**
     * Get option from config
     */
    var initialize = function () {
        var config = IPython.notebook.config;
	if (config.data.hasOwnProperty('printview2') ) {
	    var pv_config = config.data.printview2;

            if (pv_config.hasOwnProperty('nbconvert_options') ) {
                nbconvert_options = pv_config.nbconvert_options;
            }

            if (pv_config.hasOwnProperty('to_pdf') ) {
                if (typeof(pv_config.to_pdf) === "boolean") {
                    to_pdf = pv_config.to_pdf;
                }
            }
 
           if (pv_config.hasOwnProperty('add_heading_number') ) {
                if (typeof(pv_config.add_heading_number) === "boolean") {
		    if (pv_config.add_heading_number == true) {
                        add_heading_number = ' --add_heading_number ';
                    }
                }
            }

            if (pv_config.hasOwnProperty('open_tab') ) {
                if (typeof(pv_config.open_tab) === "boolean") {
                    open_tab = pv_config.open_tab;
                }
            }

            if (pv_config.hasOwnProperty('has_foreword') ) {
                if (typeof(pv_config.has_foreword) === "boolean") {
                    if (pv_config.has_foreword === true) {
                        include_foreword = ' --include_foreword ';
                    }
                }
            }

            if (pv_config.hasOwnProperty('toc_level') ) {
                toc_level = pv_config.toc_level;
            }

            if (pv_config.hasOwnProperty('include_article_summary') ) {
                if (pv_config.include_article_summary === 'none') {
                    include_article_summary = ' ';
	        } else {
		    include_article_summary = ' --include_article_summary ' + pv_config.include_article_summary;
                }
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
        var command = 'import os; os.system(\'jupyter nbconvert ' + nbconvert_options + ' \"' + name + '\"\');' + 'os.system(\'trans2std --in tmp.html --out_file ' + out_html + ' --toc_level ' + toc_level + add_heading_number + include_foreword + include_article_summary + '\');' + 'os.system(\'rm tmp.html\');'
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
            }, 'create-static-printview',  'printview2'),
        ])).find('.btn').attr('id', 'doPrintView');
        return IPython.notebook.config.loaded.then(initialize);
    };

    return {
        load_ipython_extension : load_ipython_extension
    };
});
