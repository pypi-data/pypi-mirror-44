define([
        "base/js/namespace",
        "./connectionDialog",
        "./uploadDialog",
        "./downloadDialog"
    ],
    function (IPython, connectionDialog, uploadDialog, downloadDialog) {
        var ds_type = document.createElement("SELECT")
        ds_type.size = '40'
        ds_type.className = "select-xs"
        ds_type.id = "dataset_type"

        function _onLoad() {
            // show connections
            var configure_openbis_connections = IPython.keyboard_manager.actions.register(
                connectionDialog, 'openbis-connections', 'jupyter-openBIS')

            // dnownload
            var download_datasets = IPython.keyboard_manager.actions.register(
                downloadDialog, 'openbis-dataset-download', 'jupyter-openBIS')

            // upload
            var upload_datasets = IPython.keyboard_manager.actions.register(
                uploadDialog, 'openbis-dataset-upload', 'jupyter-openBIS')

            // add button for new action
            IPython.toolbar.add_buttons_group([configure_openbis_connections, download_datasets, upload_datasets])
        }

        return {
            load_ipython_extension: _onLoad
        }
    })