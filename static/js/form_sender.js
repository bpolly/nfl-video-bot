document.querySelector('#link-form').addEventListener('submit', function(e) {
    e.preventDefault();
    document.getElementById("result--error").style.display = "none";
    removeResultRows();
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
            linkList = response.data['links']
            addFoundResultsRow(linkList.length)
            for (link of linkList) {
                addResultRow(link)
            }
            addListeners();
        })
        .catch(function(error) {
            error_message = error.response.data['error']
            document.querySelector("#result--error .result-text").innerHTML = error_message;
            document.getElementById("result--error").style.display = "block";
        });
});


function addResultRow(link) {
    var div = document.createElement('div');

    // div.id = 'result--success';
    div.className = 'result--success clearfix';

    div.innerHTML =
        '<div class="result-text">' + link + '</div>\
        <button class="button button-outline button-small float-right btn-copy">Copy</button>';

    document.getElementById('results').appendChild(div);
}

function removeResultRows() {
    var resultRows = document.querySelectorAll('.result--success');
    var resultHeader = document.getElementById('result-count');
    if(resultHeader) {
        document.getElementById('results').removeChild(resultHeader);
    }
    Array.from(resultRows).forEach(row => {
        document.getElementById('results').removeChild(row);
    });
}

function addListeners() {
    var copyButtons = document.querySelectorAll('.btn-copy');

    Array.from(copyButtons).forEach(button => {
        button.addEventListener('click', function(event) {
            const textField = document.createElement('textarea');
            var resultText = button.parentElement.querySelector('.result-text').innerText;
            textField.innerText = resultText;
            document.body.appendChild(textField);
            textField.select();
            document.execCommand('copy');
            document.body.removeChild(textField);
            button.innerHTML = 'Copied!'

            setTimeout(function(){ button.innerHTML = 'Copy' }, 10000);
        });
    });
};


function addFoundResultsRow(resultCount) {
    var div = document.createElement('h3');

    div.innerHTML = 'Found ' + resultCount + ' results'
    div.id = 'result-count'

    document.getElementById('results').appendChild(div);
}
