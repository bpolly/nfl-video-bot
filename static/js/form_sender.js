document.querySelector('#link-form').addEventListener('submit', function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    let parsedData = {};
    for(let name of formData) {
        if (typeof(parsedData[name[0]]) == "undefined") {
            let tempdata = formData.getAll(name[0]);
            if (tempdata.length > 1) {
                parsedData[name[0]] = tempdata;
            } else {
                parsedData[name[0]] = tempdata[0];
            }
        }
    }

    axios.post('/handle_data', parsedData)
        .then(function(response) {
            document.getElementById("result-text").innerHTML = response.data['links'];
            document.getElementById("result").style.display = "block";
        })
        .catch(function(error) {
            error_message = error.response.data['error']
            document.getElementById("result-text").innerHTML = error_message;
            document.getElementById("result").style.display = "block";
        });
});

var copyButtons = document.querySelectorAll('.btn-copy');

Array.from(copyButtons).forEach(button => {
    button.addEventListener('click', function(event) {
        const textField = document.createElement('textarea');
        var resultText = document.getElementById("result-text");
        textField.innerText = resultText.innerHTML;
        document.body.appendChild(textField);
        textField.select();
        document.execCommand('copy');
        document.body.removeChild(textField);
        button.innerHTML = 'Copied'

        setTimeout(function(){ button.innerHTML = 'Copy' }, 10000);
    });
});
