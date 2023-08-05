define([],
    function () {
        return {
            // connection dialog
            connection: {
                name: null,
                candidateName: null
            },

            // upload dialog
            uploadDataSetType: null,
            uploadDataSetTypes: {},
            uploadEntityIdentifier: '',
            datasetCheckboxes: [],
            fileCheckboxes: [],
            selectedFiles: [],
            unselectedDatasets: [],

            // download dialog
            selectedDatasets: new Set([])
        }
    }
)