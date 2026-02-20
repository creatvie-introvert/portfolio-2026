document.addEventListener("DOMContentLoaded", () => {
  const flag = document.getElementById("contact-success-flag");
  if (!flag) return;

  const modalEl = document.getElementById("contactSuccessModal");
  if (!modalEl) return;

  const modal = new bootstrap.Modal(modalEl);
  modal.show();
});