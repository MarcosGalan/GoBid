let activeCategory = undefined
let searchFilter = ""

function dateFormat(fecha) {
    // Obtener día, mes y año de la fecha
    let day = fecha.getDate();
    let month = fecha.getMonth() + 1; // ¡Atención! JavaScript cuenta los meses desde 0
    let year = fecha.getFullYear() % 100; // Obtener solo los dos últimos dígitos del año

    // Agregar ceros iniciales si es necesario
    day = day < 10 ? '0' + day : day;
    month = month < 10 ? '0' + month : month;
    year = year < 10 ? '0' + year : year;

    // Devolver la fecha formateada
    return day + '/' + month + '/' + year;
}

const drawProducts = (products) => {

    const listProducts = document.getElementById('productsList');
    listProducts.innerHTML = ""

    let productsFiltered = products
    if (activeCategory !== undefined) {
        productsFiltered = products.filter((product) => product.category.id === Number(activeCategory))
    }
    productsFiltered = productsFiltered.filter((product) => {
        return (searchFilter !== "") ? product.title.includes(searchFilter) : true
    })


    productsFiltered.forEach((product) => {

        const productElement = document.createElement('article')
        productElement.classList.add('product');

        const date = new Date(product.created)

        productElement.innerHTML = `
        
                    <div class="product__img">
                        <img src="${product.image}" alt="">
                    </div>

                    <div class="product__info">

                        <h3>${product.title}</h3>
                        <p>${product.subtitle}</p>

                        <p><span>Launched on:</span> ${dateFormat(date)}</p>
                        <a href="/products/product/${product.id}" class="button">View Product</a>

                    </div>
        `

        listProducts.appendChild(productElement)

    });

}

const drawCategories = (categories) => {
    const categoriesList = document.getElementById('filterList')
    categoriesList.innerHTML = ''

    let allCategory = document.createElement('li')
    allCategory.innerHTML = `<a href="#">All</a>`
    if (activeCategory === undefined) {
        allCategory.classList.add('active')
    }

    categoriesList.appendChild(allCategory)
    categories.forEach((category) => {

            const categoryLi = document.createElement('li')
            if (activeCategory == category.id) {
                categoryLi.classList.add('active')
            }

            const categoryA = document.createElement('a')
            categoryA.id = category.id
            categoryA.href = '#'
            categoryA.innerText = category.name

            categoryLi.appendChild(categoryA)
            categoriesList.appendChild(categoryLi)
        }
    )

}

let loadItems = () => {
    fetch(`/products/fetch/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            drawProducts(data.products)
            drawCategories(data.categories)
        })
        .catch(error => {
            console.error('Error en la petición:', error);
        });
}

document.getElementById("filterList").addEventListener("click", function (event) {
    // Evitar el comportamiento predeterminado del enlace
    event.preventDefault();


    // Verificar si se hizo clic en un enlace
    if (event.target.tagName === 'A') {

        activeCategory = (event.target.id) ? event.target.id : undefined
        loadItems()

    }
});

document.getElementById('searchBar').addEventListener('input', (event) => {
    searchFilter = event.target.value
    loadItems()
})

loadItems()