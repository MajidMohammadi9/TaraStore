function translateNumberJS(value, lang) {
  const maps = {
      'fa': "۰۱۲۳۴۵۶۷۸۹",
      'ar': "٠١٢٣٤٥٦٧٨٩"
  };

  return String(value).replace(/\d/g, d => maps[lang]?.[d] ?? d);
}

function convertCurrencyJS(amount, lang) {
  let rate = 1;
  let symbol = "$";
  let decimalPlaces = 2;

  if (lang === "fa") {
      rate = 92000;
      symbol = "تومان";
      decimalPlaces = 0;
  } else if (lang === "ar") {
      rate = 0.386;
      symbol = "ريال عماني";
      decimalPlaces = 3;
  }

  const total = amount * rate;
  const formatted = total.toLocaleString("en-US", {
      minimumFractionDigits: decimalPlaces,
      maximumFractionDigits: decimalPlaces
  });

  return `${translateNumberJS(formatted, lang)} ${symbol}`;
}

document.addEventListener("DOMContentLoaded", function () {
    // === Product Detail Page Script ===
    if (window.productMaxQuantity) {
      const plusButtons = document.querySelectorAll(".custom-plus");
      const minusButtons = document.querySelectorAll(".custom-minus");
      const lang = document.documentElement.lang || 'en';
  
      plusButtons.forEach((plusButton) => {
        const quantityInput = plusButton.parentElement.querySelector('input[name="quantity"]');
        const minusButton = plusButton.parentElement.querySelector(".custom-minus");
  
        if (!quantityInput) return;
  
        const maxQuantity = window.productMaxQuantity || 999;
  
        function updateQuantityButtons(value) {
          plusButton.disabled = value >= maxQuantity;
          minusButton.disabled = value <= 1;
        }

        //new function
        function updateTotalPrice(quantity, unitPrice) {
          const totalPriceElement = document.getElementById("total-price");
          if (!totalPriceElement) return;

          const rawTotal = quantity * unitPrice;
          const displayValue = convertCurrencyJS(rawTotal, lang);
          totalPriceElement.textContent = displayValue;
        }
  
        plusButton.addEventListener("click", function (e) {
          e.preventDefault();
          let current = parseInt(quantityInput.value) || 1;
          if (current < maxQuantity) {
            current += 1;
            quantityInput.value = current;
            updateQuantityButtons(current);
            updateTotalPrice(current, window.unitPrice);
          }
        });
  
        minusButton.addEventListener("click", function (e) {
          e.preventDefault();
          let current = parseInt(quantityInput.value) || 1;
          if (current > 1) {
            current -= 1;
            quantityInput.value = current;
            updateQuantityButtons(current);
            updateTotalPrice(current, window.unitPrice);
          }
        });
  
        updateQuantityButtons(parseInt(quantityInput.value));
        updateTotalPrice(parseInt(quantityInput.value), window.unitPrice);
        
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
 