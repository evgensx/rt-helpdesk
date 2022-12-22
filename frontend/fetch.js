const API_URI = 'http://' + document.location.hostname + ':8080/submit';
console.log(API_URI);
var submitButton = document.getElementsByClassName('button-sent')[0];
var form = document.forms.request;

async function asyncJson() {
    let object = {};
    let formData = new FormData(form);
    formData.forEach((value, key) => object[key] = value);

    let response = await fetch(API_URI, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        },
        body: JSON.stringify(object)
    });
    if (response.ok) {
        var formContainer = document.getElementsByClassName('form-container')[0];
        formContainer.setAttribute("style", "justify-content: center; align-items: center");
        formContainer.innerHTML = '<h2>Спасибо за обращение!</h2>';
        return response.json();
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
    return;
}

submitButton.addEventListener('click', (event) => {
    if (form.checkValidity()) {
        event.preventDefault();
        asyncJson();
    }
});