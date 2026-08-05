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
  const toggleBtn = document.getElementById("testsToggleBtn");
  const toggleLabel = document.getElementById("testsToggleLabel");
  const panel = document.getElementById("testsPanel");
  const dropdown = document.getElementById("testsDropdown");

  // فتح / إغلاق القائمة
  if (toggleBtn) {
    toggleBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      panel.classList.toggle("open");
    });
  }

  // سكر القائمة لو ضغط المستخدم برا الدروب داون
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

    // تحديث الحقل المخفي (category) بأسماء التحاليل المختارة
    categoryInput.value = selected.join(", ");

    // تحديث نص الزر
    toggleLabel.textContent = selected.length > 0
      ? selected.join(", ")
      : "Select tests...";

    // تحديث السعر
    if (priceInput) {
      priceInput.value = total.toFixed(2);
    }

    calculateRemain();
  }

  function calculateRemain() {
    if (!priceInput || !paidInput || !remainInput) return;
    const price = parseFloat(priceInput.value) || 0;
    const paid = parseFloat(paidInput.value) || 0;
    remainInput.value = (paid - price).toFixed(2);
  }

  testCheckboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", updateSelection);
  });

  if (paidInput) {
    paidInput.addEventListener("input", calculateRemain);
  }

});