function enableEdit() {
    const form = document.querySelector('form');
    const elements = form.elements;
    const editButton =document.getElementById('edit-button');
    const saveButton =document.getElementById('save-button');

    for (let i = 0; i < elements.length; i++) {
        console.log(elements)
        elements[i].removeAttribute('disabled')
    }

    editButton.classList.add('clear')
    saveButton.classList.remove('clear')

}

