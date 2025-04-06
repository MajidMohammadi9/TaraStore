
document.addEventListener("DOMContentLoaded", function () {
    // === Product Detail Page Script ===
    if (window.productMaxQuantity) {
      const plusButtons = document.querySelectorAll(".custom-plus");
      const minusButtons = document.querySelectorAll(".custom-minus");
  
      plusButtons.forEach((plusButton) => {
        const quantityInput = plusButton.parentElement.querySelector('input[name="quantity"]');
        const minusButton = plusButton.parentElement.querySelector(".custom-minus");
  
        if (!quantityInput) return;
  
        const maxQuantity = window.productMaxQuantity || 999;
  
        function updateQuantityButtons(value) {
          plusButton.disabled = value >= maxQuantity;
          minusButton.disabled = value <= 1;
        }
  
        plusButton.addEventListener("click", function (e) {
          e.preventDefault();
          let current = parseInt(quantityInput.value) || 1;
          if (current < maxQuantity) {
            quantityInput.value = current + 1;
            updateQuantityButtons(current + 1);
          }
        });
  
        minusButton.addEventListener("click", function (e) {
          e.preventDefault();
          let current = parseInt(quantityInput.value) || 1;
          if (current > 1) {
            quantityInput.value = current - 1;
            updateQuantityButtons(current - 1);
          }
        });
  
        updateQuantityButtons(parseInt(quantityInput.value));
      });
    }
  
    // === Cart Detail Page Script ===
    const cartForms = document.querySelectorAll("form input[data-max]");
  
    if (cartForms.length > 0) {
      const plusButtons = document.querySelectorAll(".custom-plus");
      const minusButtons = document.querySelectorAll(".custom-minus");
  
      plusButtons.forEach((plusButton) => {
        const quantityInput = plusButton.parentElement.querySelector('input[name="quantity"]');
        const minusButton = plusButton.parentElement.querySelector(".custom-minus");
  
        if (!quantityInput) return;
  
        const hiddenInput = plusButton.closest('form').querySelector('input[type="hidden"][data-max]');
        const maxQuantity = hiddenInput ? parseInt(hiddenInput.getAttribute('data-max')) || 999 : 999;
  
        function updateQuantityButtons(value) {
          plusButton.disabled = value >= maxQuantity;
          minusButton.disabled = value <= 1;
        }
  
        plusButton.addEventListener("click", function (e) {
          e.preventDefault();
          let current = parseInt(quantityInput.value) || 1;
          if (current < maxQuantity) {
            quantityInput.value = current + 1;
            updateQuantityButtons(current + 1);
          }
        });
  
        minusButton.addEventListener("click", function (e) {
          e.preventDefault();
          let current = parseInt(quantityInput.value) || 1;
          if (current > 1) {
            quantityInput.value = current - 1;
            updateQuantityButtons(current - 1);
          }
        });
  
        updateQuantityButtons(parseInt(quantityInput.value));
      });
    }
  });
  