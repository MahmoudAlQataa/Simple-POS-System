// Expense Tracker Lite - main JS
// It is currently empty; we will use it later for any additional interactions (such as multi-analysis or charts).

document.addEventListener("DOMContentLoaded", function () {
  console.log("Expense Tracker Lite loaded.");
});

document.addEventListener("DOMContentLoaded", function () {

  const testCheckboxes = document.querySelectorAll(".test-checkbox");
  const priceInput = document.getElementById("price");
  const paidInput = document.getElementById("paid_amount");
  const remainInput = document.getElementById("remain_amount");
  const categoryInput = document.getElementById("category");
  const discountInput = document.getElementById("discount");   // ✅ جديد
  const toggleBtn = document.getElementById("testsToggleBtn");
  const toggleLabel = document.getElementById("testsToggleLabel");
  const panel = document.getElementById("testsPanel");
  const dropdown = document.getElementById("testsDropdown");

  // Open / Close the list
  if (toggleBtn) {
    toggleBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      panel.classList.toggle("open");
    });
  }

  document.addEventListener("click", function (e) {
    if (dropdown && !dropdown.contains(e.target)) {
      panel.classList.remove("open");
    }
  });

function updateSelection() {
    const selected = [];
    let total = 0;

    testCheckboxes.forEach(function (checkbox) {
      if (checkbox.checked) {
        selected.push(checkbox.value);
        total += parseFloat(checkbox.dataset.price) || 0;
      }
    });

    categoryInput.value = selected.join(", ");

    toggleLabel.textContent = selected.length > 0
      ? selected.join(", ")
      : "Select tests...";

    applyPrice(total);
  }

  function applyPrice(total) {
    let discount = parseFloat(discountInput?.value) || 0;

    // The protection is now based on a comparison with `total` itself (since `price` always equals `total`).
    if (discount > total) {
      discount = total;
      if (discountInput) {
        discountInput.value = total.toFixed(2);
      }
    }

    // price keeps displaying the original total without the discount.
    if (priceInput) {
      priceInput.value = total.toFixed(2);
    }

    calculateRemain();
  }

  function calculateRemain() {
    if (!priceInput || !paidInput || !remainInput) return;
    const price = parseFloat(priceInput.value) || 0;
    const discount = parseFloat(discountInput?.value) || 0;   // New
    const paid = parseFloat(paidInput.value) || 0;

    // The discount applies only here.
    remainInput.value = (paid - (price - discount)).toFixed(2);
  }

  testCheckboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", updateSelection);
  });

  if (paidInput) {
    paidInput.addEventListener("input", calculateRemain);
  }

  if (discountInput) {
    discountInput.addEventListener("input", function () {
      // We recalculate the total based on the currently selected tests.
      let total = 0;
      testCheckboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
          total += parseFloat(checkbox.dataset.price) || 0;
        }
      });
      applyPrice(total);
    });
  }

});


function openEditModal(id, name, phone, paidAmount, discount) {
  const modal = document.getElementById("editModal");
  const form = document.getElementById("editForm");

  // We fill the form with the current data.
  document.getElementById("edit_name").value = name;
  document.getElementById("edit_phone").value = phone;
  document.getElementById("edit_paid_amount").value = paidAmount;
  document.getElementById("edit_discount").value = discount;

  // We specify where the form will be sent (the ID of the selected row).
  form.action = `/edit/${id}`;

  modal.style.display = "flex";
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}

// Optional: Close the modal when clicking outside the box.
document.addEventListener("click", function (e) {
  const modal = document.getElementById("editModal");
  if (e.target === modal) {
    closeEditModal();
  }
});