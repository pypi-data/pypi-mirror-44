define([
        "base/js/dialog",
        "base/js/utils",
        "jquery",
        "./state",
        "./common",
    ],
    function (dialog, utils, $, state, common) {

        var errorElements = { }
        function createErrorElement(name) {
            var element = document.createElement("STRONG")
            element.textContent = ""
            element.style.marginLeft = "8px"
            element.style.color = "red"
            errorElements[name.toLowerCase()] = element
            return element
        }
        function cleanErrors() {
            Object.keys(errorElements).forEach(key => errorElements[key].textContent="")
        }

        var spinner = document.createElement("IMG")
        spinner.className="openbis-feedback"
        spinner.src=""
        function showSpinner() {
            spinner.src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.5.8/ajax-loader.gif"
        }
        function hideSpinner() {
            spinner.src=""
        }

        function get_file_list(env, container) {
            var url = env.notebook.base_url + 'general/filelist'
        
            fetch(url)
                .then( function(response) {
                    if (response.ok) {
                        response.json()
                            .then(function(data){
                                var values = Object.keys(data.files)
                                values.sort()
                                state.fileCheckboxes = createSelectTable(values, container, false, state.selectedFiles)
                            })
                    }
                    else {
                        console.error(response.status)
                    }
                })
        }

        function get_dataset_list(env, container) {
            var datasets = env.notebook.metadata.datasets
            if (datasets != null) {
                var values = Object.keys(datasets)
                values.sort()
                state.datasetCheckboxes = createSelectTable(values, container, true, state.unselectedDatasets)
            }
        }

        function getDatasetTypes(env, connection_name, dataset_types, input_fields) {
            // get all DatasetTypes of a given connection

            var url = env.notebook.base_url + 'openbis/datasetTypes/' + connection_name
            fetch(url)
                .then(function (response) {
                    if (response.ok) {
                        response.json()
                            .then(function (data) {
                                var change_input_fields = function () {
                                    hideSpinner()
                                    cleanErrors()

                                    var oldType = state.uploadDataSetType
                                    if (oldType != null && !(oldType in state.uploadDataSetTypes)) {
                                        state.uploadDataSetTypes[oldType] = {}
                                    }

                                    state.uploadDataSetType = dataset_types.options[dataset_types.selectedIndex].value

                                    // remove existing input fields
                                    while (input_fields.firstChild) {
                                        var element = input_fields.firstChild

                                        if (element.nodeName === "INPUT" && state.uploadDataSetType != null) {
                                            state.uploadDataSetTypes[oldType][element.name] = element.value
                                        }

                                        input_fields.removeChild(element)
                                    }

                                    // for every property assignment, create an input field.
                                    for (pa of dts[dataset_types.selectedIndex].propertyAssignments) {
                                        var input_title = document.createElement("STRONG")
                                        input_title.textContent = pa.mandatory ? pa.label + " (mandatory)" : pa.label
                                        var input_error = createErrorElement('prop.'+pa.code)

                                        var input_field = document.createElement("INPUT")
                                        input_field.type = "text"
                                        input_field.name = pa.code
                                        input_field.placeholder = pa.description ? pa.description : pa.label
                                        input_field.size = 90
                                        input_field.style.width="100%"

                                        var mem = state.uploadDataSetTypes[dts[dataset_types.selectedIndex].code]
                                        if (mem == null) {
                                            mem = {}
                                        }
                                        input_field.value = pa.code in mem ? mem[pa.code] : ""

                                        input_fields.appendChild(input_title)
                                        input_fields.appendChild(input_error)
                                        input_fields.appendChild(input_field)
                                        input_fields.appendChild(document.createElement("BR"))
                                    }
                                }
                                dataset_types.onchange = change_input_fields

                                // remove the old and add the new dataset-types
                                dts = data.dataSetTypes
                                while (dataset_types.firstChild) {
                                    dataset_types.removeChild(dataset_types.firstChild);
                                }
                                var index = 0
                                var selectedIndex = -1
                                for (dt of dts) {
                                    var option = document.createElement("OPTION")
                                    option.value = dt.code
                                    option.textContent = dt.description ? dt.code + ": " + dt.description : dt.code
                                    dataset_types.appendChild(option)

                                    if (dt.code === state.uploadDataSetType) {
                                        selectedIndex = index
                                    }
                                    index++
                                }

                                dataset_types.selectedIndex = selectedIndex === -1 ? 0 : selectedIndex
                                // change the input fields, since we just received new datasetTypes
                                change_input_fields()

                            })
                            .catch(function (error) {
                                console.error("Error while parsing dataset types", error)
                            })

                    } else {
                        while (dataset_types.firstChild) {
                            dataset_types.removeChild(dataset_types.firstChild);
                        }
                    }
                })
                .catch(function (error) {
                    console.error("Error while fetching dataset types:", error)
                })
        }

        function createSelectTable(values, container, checked, overrides) {

            var table = document.createElement("TABLE")
            table.className = 'table-bordered table-striped table-condensed'
            table.style.width = "100%"
            
            var body = table.createTBody()

            var checkboxes = []
            values.forEach( value => {
                var row = body.insertRow()
                var checkbox = document.createElement("INPUT")
                checkbox.type = "checkbox"
                checkbox.value = value
                checkbox.checked = overrides.includes(value) ? !checked :  checked
                checkboxes.push(checkbox)
                row.insertCell().appendChild(checkbox)
                var valueCell = row.insertCell()
                valueCell.textContent = value
                valueCell.style.width = "100%"
            })
            container.appendChild(table)

            return checkboxes
        }

        return {
            help: 'upload Notebook and Data to openBIS',
            icon: 'fa-upload',
            help_index: '',
            handler: function (env) {

                var main_error = createErrorElement('main')

                var dst_title = document.createElement("STRONG")
                dst_title.textContent = "DataSet type"
                var dataset_types = document.createElement("SELECT")
                dataset_types.id = "dataset_type"
                dataset_types.className = "form-control select-xs"
                dataset_types.style.marginLeft = 0
                dataset_types.style.padding = 0

                var input_fields = document.createElement("DIV")
                input_fields.setAttribute("id", "upload-input-fields");

                getDatasetTypes(env, state.connection.name, dataset_types, input_fields)

                var sample_title = document.createElement("STRONG")
                sample_title.textContent = "Sample or Experiment identifier/permId"

                var sample_error = createErrorElement('entityIdentifier')

                var entityIdentifier = document.createElement("INPUT")
                entityIdentifier.type = "text"
                entityIdentifier.name = 'entityIdentifier'
                entityIdentifier.placeholder = "Sample or Experiment identifier/permId"
                entityIdentifier.value = state.uploadEntityIdentifier
                entityIdentifier.size = "90"
                entityIdentifier.style.width="100%"

                var ds_title = document.createElement("STRONG")
                var dataSetListContainer = document.createElement("DIV")
                if (env.notebook.metadata.datasets) {
                    ds_title.textContent = "DataSets"
                    dataSetListContainer.style.maxHeight="150px"
                    dataSetListContainer.style.overflow="auto"
                    get_dataset_list(env, dataSetListContainer)
                }

                var files_title = document.createElement("STRONG")
                files_title.textContent = "Files"
                var fileListContainer = document.createElement("DIV")
                fileListContainer.style.maxHeight="150px"
                fileListContainer.style.overflow="auto"
                get_file_list(env, fileListContainer)
                
                var inputs = document.createElement("DIV")
                inputs.style.marginTop = '10px'
                inputs.appendChild(main_error)
                inputs.appendChild(spinner)
                inputs.appendChild(document.createElement("BR"))
                inputs.appendChild(dst_title)
                inputs.appendChild(dataset_types)
                inputs.appendChild(input_fields)
                inputs.appendChild(sample_title)
                inputs.appendChild(sample_error)
                inputs.appendChild(entityIdentifier)
                inputs.appendChild(ds_title)
                inputs.appendChild(dataSetListContainer)
                inputs.appendChild(files_title)
                inputs.appendChild(fileListContainer)

                var uploadDialogBox = $('<div/>').append(inputs)

                function saveState() {
                    state.uploadDataSetTypes[state.uploadDataSetType] = {}
                    for (element of input_fields.children) {
                        if (element.nodeName === "INPUT" && state.uploadDataSetType != null) {
                            state.uploadDataSetTypes[state.uploadDataSetType][element.name] = element.value
                        }
                    }
                    state.uploadEntityIdentifier = entityIdentifier.value
                    state.unselectedDatasets = state.datasetCheckboxes.filter(cb => !cb.checked).map(cb => cb.value)
                    state.selectedFiles = state.fileCheckboxes.filter(cb => cb.checked).map(cb => cb.value)
                }

                function onOk() {
                    var connection_name = state.connection.name

                    if (!connection_name) {
                        alert("No connection selected")
                        return false
                    }

                    var uploadUrl = env.notebook.base_url + 'openbis/dataset/' + connection_name

                    var notebook = IPython.notebook
                    var files = state.fileCheckboxes.filter(cb => cb.checked).map(cb => cb.value)
                    var re = /\/notebooks\/(.*?)$/
                    var filepath = window.location.pathname.match(re)[1]
                    files.push(filepath)
                    
                    var props = {}
                    for (input of $('#upload-input-fields').find('input')) {
                        props[input.name] = input.value
                    }

                    var dataSetInfo = {
                        "type": dataset_types.value,
                        "files": files,
                        "parents": state.datasetCheckboxes.filter(cb => cb.checked).map(cb => cb.value),
                        "entityIdentifier": entityIdentifier.value,
                        "props": props
                    }

                    var settings = {
                        url: uploadUrl,
                        processData: false,
                        type: 'POST',
                        dataType: 'json',
                        data: JSON.stringify(dataSetInfo),
                        contentType: 'application/json',
                        success: function (data) {
                            saveState()
                            $('div.modal').remove()
                            $('div.modal-backdrop').remove()
                            common.createFeedback('success', data.statusText)

                            // write statusText from returned data to notebooks metadata
                            if (typeof notebook.metadata.openbis === 'undefined') {
                                notebook.metadata.openbis = {}
                            }
                            if (typeof notebook.metadata.openbis.permIds === 'undefined') {
                                notebook.metadata.openbis.permIds = {}
                            }
                            if (data.permId) {
                                notebook.metadata.openbis.permIds[data.permId] = data.statusText
                            }
                        },
                        error: function (data) {
                            hideSpinner()

                            if ("errors" in data.responseJSON) {
                                var errors = data.responseJSON.errors
                                for (error of errors) {
                                    let key, value
                                    Object.keys(error).forEach(k => {
                                        key = k.toLowerCase()
                                        value = error[k]
                                    })
                                    errorElements[key in errorElements ? key : "main"].textContent = value
                                }
                            } else {
                                errorElements["main"].textContent = "Server error"
                            }
                        }
                    }

                    showSpinner()
                    cleanErrors()
                    utils.ajax(settings)
                    return false
                }

                function onCancel() {
                    saveState()
                    return true
                }

                if (IPython.notebook.dirty === true) {
                    dialog.modal({
                        body: 'Please save the notebook before uploading it to openBIS.',
                        title: 'Save notebook first',
                        buttons: {
                            'Back': {}
                        },
                        notebook: env.notebook,
                        keyboard_manager: env.notebook.keyboard_manager
                    })
                } else {
                    dialog.modal({
                        body: uploadDialogBox,
                        title: 'Upload openBIS DataSet',
                        buttons: {
                            'Cancel': {
                                click: onCancel
                            },
                            'Upload': {
                                class: 'btn-primary btn-large',
                                click: onOk
                            }
                        },
                        notebook: env.notebook,
                        keyboard_manager: env.notebook.keyboard_manager
                    })
                }
            }
        }
    }
)