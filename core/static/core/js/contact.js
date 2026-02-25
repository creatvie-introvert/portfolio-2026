document.addEventListener("DOMContentLoaded", () => {
  /**
   * =========================
   * Cookie Consent + GA Loader
   * =========================
   */

  const GA_MEASUREMENT_ID = "G-K7B6E15QF5";
  const CONSENT_KEY = "cookie_consent";

  const banner = document.getElementById("cookieBanner");
  const acceptBtn = document.getElementById("acceptCookies");
  const rejectBtn = document.getElementById("rejectCookies");

  function loadAnalytics() {
    // Prevent double-loading
    if (window.__gaLoaded) return;

    // Inject gtag script
    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(script);

    // Init gtag
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    window.gtag = gtag;

    gtag("js", new Date());
    gtag("config", GA_MEASUREMENT_ID);

    window.__gaLoaded = true;
  }

  function hasAcceptedCookies() {
    return localStorage.getItem(CONSENT_KEY) === "accepted";
  }

  function showBannerIfNeeded() {
    const consent = localStorage.getItem(CONSENT_KEY);
    if (!consent && banner) banner.style.display = "block";
  }

  // If already accepted, load GA immediately on page load
  if (hasAcceptedCookies()) {
    loadAnalytics();
  } else {
    showBannerIfNeeded();
  }

  // Accept
  if (acceptBtn) {
    acceptBtn.addEventListener("click", () => {
      localStorage.setItem(CONSENT_KEY, "accepted");
      if (banner) banner.style.display = "none";
      loadAnalytics();
    });
  }

  // Reject
  if (rejectBtn) {
    rejectBtn.addEventListener("click", () => {
      localStorage.setItem(CONSENT_KEY, "rejected");
      if (banner) banner.style.display = "none";
    });
  }

  /**
   * =========================
   * Contact success/error logic
   * =========================
   */

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

    // Track conversion ONLY if cookies accepted
    if (hasAcceptedCookies()) {
      // Ensure GA exists (in case user accepted on this page)
      loadAnalytics();

      if (typeof window.gtag === "function") {
        window.gtag("event", "contact_submit", {
          page_path: window.location.pathname,
          page_title: document.title,
          referrer: document.referrer,
          project_source: document.referrer.includes("/portfolio/work/")
            ? document.referrer
            : "direct_or_unknown",
        });
      }
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