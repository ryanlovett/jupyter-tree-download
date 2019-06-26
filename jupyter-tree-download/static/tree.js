define([
    'jquery',
    'base/js/utils',
    'base/js/namespace'
], function (
    $, utils, Jupyter
) {

    var load_ipython_extension = function () {
        $(".col-sm-8.no-padding").attr('class', 'col-sm-4 no-padding');
        $(".col-sm-4.no-padding.tree-buttons").attr('class', 'col-sm-8 no-padding tree-buttons');

        $('#notebook_toolbar .pull-right').prepend(
          $('<div>').addClass('btn-group').attr('id', 'tree-download').prepend(
               '<button class="btn btn-xs btn-default" title="Download">Download</button>'
          ).click(function() {
			var dir_path = document.body.getAttribute('data-notebook-path');
			console.log("dir_path: " + dir_path);

			var baseUrl = document.location.origin + document.body.getAttribute('data-base-url');
			/* we name the file based on what the client sees as the hostname */
			var hostname = document.location.hostname;
            window.location.href = baseUrl + 'tree-download?name=' + hostname + '&path=' + dir_path;
          })
        )
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };

  });
