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


function openEditModal(id, name, phone, paidAmount, discount, gender, doctorName) {
  const modal = document.getElementById("editModal");
  const form = document.getElementById("editForm");

  // We fill the form with the current data.
  document.getElementById("edit_name").value = name;
  document.getElementById("edit_phone").value = phone;
  document.getElementById("edit_paid_amount").value = paidAmount;
  document.getElementById("edit_discount").value = discount;
  document.getElementById("edit_gender").value = gender;
  document.getElementById("edit_doctor_name").value = doctorName || "";

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

// Customer search
document.addEventListener("DOMContentLoaded", function () {
  const nameInput = document.getElementById("name");
  const customerIdInput = document.getElementById("customer_id");
  const resultsBox = document.getElementById("customerResults");
  const phoneInput = document.querySelector('input[name="phone"]');
  const genderSelect = document.getElementById("gender");

  if (!nameInput || !resultsBox) return;

  let debounceTimer;

  nameInput.addEventListener("input", function () {
    customerIdInput.value = ""; // أي تعديل يدوي بالاسم يلغي الربط بزبون سابق

    clearTimeout(debounceTimer);
    const q = nameInput.value.trim();

    if (q.length < 1) {
      resultsBox.innerHTML = "";
      resultsBox.classList.remove("open");
      return;
    }

    debounceTimer = setTimeout(function () {
      fetch(`/customer/search?q=${encodeURIComponent(q)}`)
        .then((res) => res.json())
        .then((data) => {
          if (!data.length) {
            resultsBox.innerHTML = "";
            resultsBox.classList.remove("open");
            return;
          }

          resultsBox.innerHTML = data
            .map(
              (c) =>
                `<div class="customer-result-item" data-id="${c.id}" data-name="${c.name}" data-phone="${c.phone}" data-gender="${c.gender}">
                  ${c.name} — ${c.phone || "-"} — ${c.gender}
                </div>`
            )
            .join("");
          resultsBox.classList.add("open");
        });
    }, 250);
  });

  resultsBox.addEventListener("click", function (e) {
    const item = e.target.closest(".customer-result-item");
    if (!item) return;

    nameInput.value = item.dataset.name;
    customerIdInput.value = item.dataset.id;
    if (phoneInput) phoneInput.value = item.dataset.phone;
    if (genderSelect) genderSelect.value = item.dataset.gender;

    resultsBox.innerHTML = "";
    resultsBox.classList.remove("open");
  });

  document.addEventListener("click", function (e) {
    if (!resultsBox.contains(e.target) && e.target !== nameInput) {
      resultsBox.classList.remove("open");
    }
  });
});

// Actions dropdown (generic, works for any table using .actions-dropdown)
document.addEventListener("click", function (e) {
  const trigger = e.target.closest(".actions-trigger");

  // close all open menus first
  document.querySelectorAll(".actions-menu.open").forEach(function (menu) {
    if (!trigger || menu !== trigger.nextElementSibling) {
      menu.classList.remove("open");
    }
  });

  if (trigger) {
    const menu = trigger.nextElementSibling;
    menu.classList.toggle("open");
    return;
  }

  if (!e.target.closest(".actions-menu")) {
    document.querySelectorAll(".actions-menu.open").forEach(function (menu) {
      menu.classList.remove("open");
    });
  }
});