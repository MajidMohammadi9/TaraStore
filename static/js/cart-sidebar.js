document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener('click', function (event) {
    const miniCart = document.getElementById('miniCart');
    const cartSidebarHeader = document.querySelector('.cart-sidebar-header');
  
    
    if (
      !miniCart.contains(event.target) &&
      !cartSidebarHeader.contains(event.target) 
    ) {
      miniCart.classList.remove('active'); 
    }
  });
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
  
