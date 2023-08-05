define(
    [
        "base/js/dialog",
        "jquery",
        "./state",
        "./connections"
    ],
    function (dialog, $, state, connections) {

        var currentDownloadPath = null

        function show_available_connections(env, data, conn_table, onclick_cbf) {
            if (!currentDownloadPath) {
                currentDownloadPath = data.cwd
            }

            var table = document.createElement("TABLE")
            table.className = 'table-bordered table-striped table-condensed'
            var thead = table.createTHead()
            var thead_row = thead.insertRow(0)
            var titles = ['', 'Name', 'URL', 'Status', 'Username / Password']
            for (title of titles) {
                thead_row.insertCell().textContent = title
            }

            tbody = table.createTBody()
            for (connection of data.connections) {
                var conn = document.createElement("INPUT")
                conn.type = "radio"
                conn.name = "connection_name"
                conn.value = connection.name
                conn.setAttribute("url", connection.url)

                conn.checked = connection.name === state.connection.candidateName;
                if (onclick_cbf === undefined) {
                    conn.onclick = function () {
                        state.connection.candidateName = this.value
                    }
                } else {
                    conn.onclick = onclick_cbf
                }

                var row = tbody.insertRow()
                row.insertCell().appendChild(conn)
                row.insertCell().textContent = connection.name
                row.insertCell().textContent = connection.url

                var status_cell = row.insertCell()

                var status_badge = document.createElement("SPAN")
                status_badge.id = connection.name + "-badge"
                status_badge.textContent = connection.status
                if (connection.status === "connected") {
                    status_badge.className = "label label-success"
                } else {
                    status_badge.className = "label label-danger"
                }
                status_cell.appendChild(status_badge)

                var username = document.createElement("INPUT")
                username.type = "text"
                username.name = "username"
                username.autocomplete = "on"
                username.value = connection.username
                username.setAttribute("form", connection.name)

                var password = document.createElement("INPUT")
                password.type = "password"
                password.name = "password"
                password.autocomplete = "current-password"
                password.value = connection.password
                password.setAttribute("form", connection.name)

                // Username / Password form
                var pwform = document.createElement("FORM")
                pwform.id = connection.name
                pwform.onsubmit = function (event) {
                    var form_data = new FormData(this)
                    var status_badge = document.getElementById(this.id + "-badge")
                    connections.connect(env, this.id,
                            form_data.get("username"), form_data.get("password")
                        )
                        .then(function (response) {
                            //console.log(response)
                            if (status_badge.nextElementSibling !== null) {
                                status_badge.parentNode.removeChild(status_badge.nextElementSibling)
                            }
                            if (response.ok) {
                                status_badge.textContent = "connected"
                                status_badge.className = "label label-success"
                            } else {
                                status_badge.textContent = "not connected"
                                status_badge.className = "label label-danger"
                                message = document.createElement("p")
                                if (response.status === 401) {
                                    message.textContent = "username/password incorrect"
                                } else if (response.status === 500) {
                                    message.textContent = "Connection error"
                                } else {
                                    message.textContent = "General error"
                                }
                                status_badge.parentNode.insertBefore(message, status_badge.nextSibling)
                            }
                        })
                        .catch(error => console.error("Error while attempting to reconnect: ", error))

                    return false
                }


                var connect_button = document.createElement("BUTTON")
                connect_button.className = "btn btn-primary btn-xs"
                connect_button.textContent = "connect"

                pwform.appendChild(username)
                pwform.appendChild(password)
                pwform.appendChild(connect_button)

                var cell = row.insertCell()
                cell.appendChild(pwform)
            }

            // add row for new connection
            var row = tbody.insertRow()

            var conn_form = document.createElement("FORM")
            conn_form.id = "new_connection"
            conn_form.onsubmit = function (event) {
                var inputs = document.querySelectorAll("input[form=new_connection]")

                data = {}
                for (input of inputs) {
                    data[input.name] = input.value
                }
                for (missing of ['connection_name', 'url', 'username', 'password']) {
                    if (data[missing] === "") {
                        alert("Please provide: " + missing)
                        return false
                    }
                }
                connections.create(env, data.connection_name, data.url, data.username, data.password)
                    .then(function (response) {
                        if (response.ok) {
                            response.json()
                                .then(function (data) {
                                    show_available_connections(env, data, conn_table)
                                })
                        }
                    })
                return false
            }
            var conn_name = document.createElement("INPUT")
            conn_name.type = "input"
            conn_name.name = "connection_name"
            conn_name.setAttribute("form", conn_form.id)
            conn_name.placeholder = "openBIS instance name"
            row.insertCell().appendChild(conn_form)
            row.insertCell().appendChild(conn_name)

            var conn_url = document.createElement("INPUT")
            conn_url.type = "input"
            conn_url.name = "url"
            conn_url.setAttribute("form", conn_form.id)
            conn_url.placeholder = "https://openbis.domain:port"
            row.insertCell().appendChild(conn_url)
            row.insertCell()

            var username = document.createElement("INPUT")
            username.autocomplete = "off"
            username.type = "text"
            username.name = "username"
            username.setAttribute("form", conn_form.id)
            username.placeholder = "username"
            var password = document.createElement("INPUT")
            password.type = "password"
            password.name = "password"
            password.autocomplete = "new-password"
            password.setAttribute("form", conn_form.id)
            var create_btn = document.createElement("BUTTON")
            create_btn.setAttribute("form", conn_form.id)
            create_btn.textContent = "create"
            var uname_pw_cell = row.insertCell()
            uname_pw_cell.appendChild(username)
            uname_pw_cell.appendChild(password)
            uname_pw_cell.appendChild(create_btn)

            conn_table.innerHTML = ""
            table_title = document.createElement("STRONG")
            table_title.textContent = "Please choose a connection"
            conn_table.appendChild(table_title)
            conn_table.appendChild(table)
        }

        return {
            help: 'configure openBIS connections',
            icon: 'fa-sliders',
            help_index: '',
            handler: function (env) {
                conn_table = document.createElement("DIV")
                var dst_title = document.createElement("STRONG")
                dst_title.textContent = "DataSet type"
                var dataset_types = document.createElement("SELECT")
                dataset_types.id = "dataset_type"
                dataset_types.className = "form-control select-xs"

                var input_fields = document.createElement("DIV")
                conn_table.id = "openbis_connections"

                var onclick_cbf = function () {
                    state.connection.candidateName = this.value
                }

                connections.list(env)
                    .done(function (data) {
                        show_available_connections(env, data, conn_table, onclick_cbf)
                    })
                    .fail(function (data) {
                        alert(data.status)
                    })

                var uploadDialogBox = $('<div/>').append(conn_table)

                function onOk() {
                    state.connection.name = state.connection.candidateName
                }

                function onCancel() {
                    state.connection.candidateName = state.connection.name
                }

                dialog.modal({
                    body: uploadDialogBox,
                    title: 'Choose openBIS connection',
                    buttons: {
                        'Cancel': {
                            click: onCancel
                        },
                        'Choose connection': {
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
)