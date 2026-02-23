document.addEventListener("DOMContentLoaded", () => {
  const successFlag = document.getElementById("contact-success-flag");
  const errorFlag = document.getElementById("contact-error-flag");

  const successModalEl = document.getElementById("contactSuccessModal");
  const errorModalEl = document.getElementById("contactErrorModal");

  const form = document.querySelector(".contact-form form");

  // SUCCESS
  if (successFlag && successModalEl) {
    const modal = new bootstrap.Modal(successModalEl);
    modal.show();

    // Clear form
    if (form) {
      form.reset();
    }

    // Focus modal for accessibility
    successModalEl.addEventListener("shown.bs.modal", () => {
      successModalEl.querySelector(".btn").focus();
    });
  }

  // ERROR
  if (errorFlag && errorModalEl) {
    const modal = new bootstrap.Modal(errorModalEl);
    modal.show();

    errorModalEl.addEventListener("shown.bs.modal", () => {
      errorModalEl.querySelector(".btn").focus();
    });
  }
});