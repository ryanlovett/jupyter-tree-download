define([
    'jquery',
    'base/js/utils',
], function (
    $, utils
) {

    var load_ipython_extension = function () {
        $(".col-sm-8.no-padding").attr('class', 'col-sm-4 no-padding');
        $(".col-sm-4.no-padding.tree-buttons").attr('class', 'col-sm-8 no-padding tree-buttons');

        $('#notebook_toolbar .pull-right').prepend(
          $('<div>').addClass('btn-group').attr('id', 'tree-download').prepend(
               '<button class="btn btn-xs btn-default" title="Download">Download</button>'
          ).click(function() {
            var dirPath = utils.get_body_data('notebookPath')
			console.log("dir_path: " + dirPath);

            var baseUrl = utils.get_body_data('baseUrl')

			/* we name the file based on what the client sees as the hostname
             * because it is usually a jupyterhub */
			var hostname = document.location.hostname;
            window.location.href = baseUrl + 'tree-download?name=' + hostname + '&path=' + dirPath;
          })
        )
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };

  });
