define([
        "base/js/namespace"
    ],
    function (IPython) {

        function createFeedback(type, content) {
            var close = document.createElement("BUTTON")
            close.className = "close"
            close.setAttribute("data-dismiss", "alert")
            close.setAttribute("aria-label", "Close")
            var x = document.createElement("SPAN")
            x.setAttribute("aria-hidden", true)
            x.innerHTML = "&times;"
            close.appendChild(x)

            var feedbackBox = document.createElement("DIV")
            feedbackBox.className = "openbis-feedback alert alert-dismissible alert-" + type
            feedbackBox.setAttribute("role", "alert")
            feedbackBox.innerHTML = content
            feedbackBox.prepend(close)

            var nb_container = document.getElementById('notebook-container')
            nb_container.prepend(feedbackBox)
        }

        function getCookie(cname) {
            var name = cname + "=";
            var decodedCookie = decodeURIComponent(document.cookie);
            var ca = decodedCookie.split(';');
            for(var i = 0; i <ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) === ' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(name) === 0) {
                    return c.substring(name.length, c.length);
                }
            }
            return "";
        }

        return {
            createFeedback: createFeedback,
            getCookie: getCookie
        }
    }
)