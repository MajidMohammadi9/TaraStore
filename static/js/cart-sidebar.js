// document.addEventListener("DOMContentLoaded", function () {
//   document.addEventListener('click', function (event) {
//     const miniCart = document.getElementById('miniCart');
//     const cartSidebarHeader = document.querySelector('.cart-sidebar-header');
  
    
//     if (
//       !miniCart.contains(event.target) &&
//       !cartSidebarHeader.contains(event.target) 
//     ) {
//       miniCart.classList.remove('active'); 
//     }
//   });
//     const links = document.querySelectorAll('a[href="#miniCart"]');
//     links.forEach(function (link) {
//       link.addEventListener("click", function (event) {
//         event.preventDefault();
//         toggleMiniCart();
//       });
//     });
//   });
  
// function toggleMiniCart() {
//   const miniCart = document.getElementById("miniCart");
//   miniCart.classList.toggle("active");
// }

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOMContentLoaded fired");

  const miniCart = document.getElementById('miniCart');
  const cartSidebarHeader = document.querySelector('.cart-sidebar-header');

  console.log("miniCart:", miniCart);
  console.log("cartSidebarHeader:", cartSidebarHeader);

  // Only proceed if both elements are found
    if (!miniCart || !cartSidebarHeader) {
    console.error("miniCart or cartSidebarHeader not found in the DOM!");
    return; // Exit if elements not found
  }

  document.addEventListener('click', function (event) {
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
  console.log('toggleMiniCart');
  if(miniCart)
    miniCart.classList.toggle("active");
}
