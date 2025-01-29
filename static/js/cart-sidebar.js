document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll('a[href="#miniCart"]');
    links.forEach(function (link) {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        toggleMiniCart();
      });
    });
  });
  
  function toggleMiniCart() {
    const miniCart = document.getElementById("miniCart");
    miniCart.classList.toggle("active");
  }
  