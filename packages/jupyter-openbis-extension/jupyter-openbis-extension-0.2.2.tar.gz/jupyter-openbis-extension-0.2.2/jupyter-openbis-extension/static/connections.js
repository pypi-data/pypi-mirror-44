define([
        "base/js/utils",
        "./common"
    ],
    function (utils, common) {

        function list(env) {

            var connectionsUrl = env.notebook.base_url + 'openbis/conns'
            var settings = {
                url: connectionsUrl,
                processData: false,
                type: 'GET',
                dataType: 'json',
                contentType: 'application/json'
            }
            return utils.ajax(settings)
        }


        function connect(env, connection, username, password) {
            var url = env.notebook.base_url + 'openbis/conn/' + connection
            body = {
                "username": username,
                "password": password
            }

            var xsrf_token = common.getCookie('_xsrf')
            return fetch(url, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-XSRFToken": xsrf_token,
                    "credentials": "same-origin",
                },
                body: JSON.stringify(body)
            })
        }

        function create(env, connection_name, connection_url, username, password) {
            var endpoint = env.notebook.base_url + 'openbis/conns'
            body = {
                "name": connection_name,
                "url": connection_url,
                "username": username,
                "password": password
            }

            var xsrf_token = common.getCookie('_xsrf')
            return fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-XSRFToken": xsrf_token,
                    "credentials": "same-origin",
                },
                body: JSON.stringify(body)
            })
        }

        return {
            list: list,
            create: create,
            connect: connect
        }
    }
)