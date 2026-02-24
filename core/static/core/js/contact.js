document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const status = params.get("contact");

  if (!status) return;

  if (status === "success") {
    const modalEl = document.getElementById("contactSuccessModal");
    if (modalEl) {
      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    }

    // Clear form after success
    const form = document.querySelector(".contact-form form");
    if (form) form.reset();

    // ✅ Track conversion with project context
    if (typeof gtag === "function") {
      gtag("event", "contact_submit", {
        page_path: window.location.pathname,
        page_title: document.title,
        referrer: document.referrer,
        project_source: document.referrer.includes("/portfolio/work/")
          ? document.referrer
          : "direct_or_unknown"
      });
    }
  }

  if (status === "error") {
    const modalEl = document.getElementById("contactErrorModal");
    if (modalEl) {
      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    }
  }
});