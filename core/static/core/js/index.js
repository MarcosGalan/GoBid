const profile = document.querySelector('.dropdown-activator');
const dropdown = document.getElementById('dropdown');
profile.addEventListener('click', (e) => {
    dropdown.classList.toggle('clear');

});