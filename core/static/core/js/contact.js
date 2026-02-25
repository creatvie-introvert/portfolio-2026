document.addEventListener("DOMContentLoaded", () => {
  // -----------------------------
  // Cookie consent (GA4)
  // -----------------------------
  const GA_MEASUREMENT_ID = "G-K7B6E15QF5"; // ✅ your ID
  const CONSENT_KEY = "lbr_cookie_consent"; // "accepted" | "rejected"

  const banner = document.getElementById("cookieBanner");
  const acceptBtn = document.getElementById("acceptCookies");
  const rejectBtn = document.getElementById("rejectCookies");

  const params = new URLSearchParams(window.location.search);
  const debugMode = params.get("ga_debug") === "1";

  function hasGtag() {
    return typeof window.gtag === "function";
  }

  function hideBanner() {
    if (banner) banner.style.display = "none";
  }

  function showBanner() {
    if (banner) banner.style.display = "block";
  }

  function getConsent() {
    return localStorage.getItem(CONSENT_KEY); // accepted | rejected | null
  }

  function setConsent(value) {
    localStorage.setItem(CONSENT_KEY, value);
  }

  function grantAnalytics() {
    if (!hasGtag()) return;

    gtag("consent", "update", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });

    if (debugMode) {
      gtag("set", "debug_mode", true);
    }

    // Enable GA config now that consent is granted
    gtag("config", GA_MEASUREMENT_ID, {
      anonymize_ip: true,
      send_page_view: true,
    });

    // Force an immediate page_view (helps Realtime update instantly)
    gtag("event", "page_view", {
      page_path: window.location.pathname + window.location.search,
      page_title: document.title,
    });
  }

  function denyAnalytics() {
    if (!hasGtag()) return;

    gtag("consent", "update", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
  }

  // On load: apply saved choice (or show banner)
  const savedConsent = getConsent();

  if (!savedConsent) {
    showBanner();
  } else {
    hideBanner();
    if (savedConsent === "accepted") grantAnalytics();
    if (savedConsent === "rejected") denyAnalytics();
  }

  // Button handlers
  if (acceptBtn) {
    acceptBtn.addEventListener("click", () => {
      setConsent("accepted");
      hideBanner();
      grantAnalytics();
    });
  }

  if (rejectBtn) {
    rejectBtn.addEventListener("click", () => {
      setConsent("rejected");
      hideBanner();
      denyAnalytics();
    });
  }

  // -----------------------------
  // Contact form success tracking
  // -----------------------------
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

    // Only track if user accepted analytics
    if (getConsent() === "accepted" && hasGtag()) {
      gtag("event", "contact_submit", {
        page_path: window.location.pathname,
        page_title: document.title,
        referrer: document.referrer,
        project_source: localStorage.getItem("lbr_last_project") || "direct_or_unknown",
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