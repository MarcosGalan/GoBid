simplyCountdown('#cuenta', {
	year: 2023, 
	month: 12, 
	day: 19, 
	hours: 7, 
	minutes: 31, 
	seconds: 0, 
	words: { 
		days: 'Día',
		hours: 'Hora',
		minutes: 'Minuto',
		seconds: 'Segundo',
		pluralLetter: 's'
	},
	plural: true, 
	inline: false, 
	inlineClass: 'simply-countdown-inline', 
	
	enableUtc: true, 
	onEnd: function() {
		document.getElementById('portada').classList.add('oculta');
		return; 
	}, 
	refresh: 1000, 
	sectionClass: 'simply-section', 
	amountClass: 'simply-amount', 
	wordClass: 'simply-word', 
	zeroPad: false,
	countUp: false
});


/*carrousel*/
let currentIndex = 0;
const slides = document.querySelectorAll('.carousel img');
const carouselContainer = document.querySelector('.carousel');

// Clonar las imágenes y agregarlas al final del carrusel
const clonedSlides = Array.from(slides).map((slide) => slide.cloneNode(true));
clonedSlides.forEach((clonedSlide) => {
    carouselContainer.appendChild(clonedSlide);
});

function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    updateCarousel();
}

function updateCarousel() {
    const newPosition = -currentIndex * 100 + '%';
    carouselContainer.style.transition = 'transform 0.5s ease-in-out';
    carouselContainer.style.transform = 'translateX(' + newPosition + ')';
}

// Reiniciar el carrusel al final
function handleTransitionEnd() {
    if (currentIndex === slides.length) {
        currentIndex = 0;
        carouselContainer.style.transition = 'none';
        updateCarousel();
    }
}

carouselContainer.addEventListener('transitionend', handleTransitionEnd);

// Mostrar la primera imagen al cargar la página
updateCarousel();

// Cambiar a la siguiente imagen cada 7 segundos (ajustado a 7 segundos según tu código)
setInterval(nextSlide, 7000);
