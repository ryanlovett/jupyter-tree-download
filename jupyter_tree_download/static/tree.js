define([
    'jquery',
    'base/js/utils',
], function (
    $, utils
) {

    var load_ipython_extension = function () {

        $('#notebook_toolbar .pull-right').prepend(
          $('<div>').addClass('btn-group').attr('id', 'tree-download').prepend(
               '<button class="btn btn-xs btn-default" title="Download Directory">Download Directory</button>'
          ).click(function() {
            // $('body').data() isn't updated when the user navigates
            // from folder to folder using /tree, so the method below
            // won't have the correct value.
            //var dirPath = utils.get_body_data('notebookPath')
            var dirPath = document.body.getAttribute('data-notebook-path');
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
