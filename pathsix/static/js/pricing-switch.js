document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("price-toggle");
  toggle.addEventListener("change", function () {
    const monthlyOptions = document.querySelectorAll(".monthly");
    const yearlyOptions = document.querySelectorAll(".yearly");

    if (this.checked) {
      monthlyOptions.forEach((option) => (option.style.display = "none"));
      yearlyOptions.forEach((option) => (option.style.display = "block"));
    } else {
      monthlyOptions.forEach((option) => (option.style.display = "block"));
      yearlyOptions.forEach((option) => (option.style.display = "none"));
    }
  });
});
