document.addEventListener("DOMContentLoaded", function() {
  const wrapper = document.querySelector('.swiper-wrapper');
  const slides = document.querySelectorAll('.swiper-slide');
  const nextButton = document.querySelector('.swiper-button-next');
  const prevButton = document.querySelector('.swiper-button-prev');
  const pagination = document.querySelector('.swiper-pagination');

  let currentIndex = 0;

  function updateSlides() {
    wrapper.style.transform = `translateX(-${currentIndex * 100}%)`;
    updatePagination();
  }

  function updatePagination() {
    const dots = pagination.querySelectorAll('div');
    dots.forEach(dot => dot.classList.remove('active'));
    dots[currentIndex].classList.add('active');
  }

  slides.forEach((_, index) => {
    const dot = document.createElement('div');
    dot.addEventListener('click', () => {
      currentIndex = index;
      updateSlides();
    });
    pagination.appendChild(dot);
  });

  nextButton.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % slides.length;
    updateSlides();
  });

  prevButton.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    updateSlides();
  });

  updateSlides();
});
