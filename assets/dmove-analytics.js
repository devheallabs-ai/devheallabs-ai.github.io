/* Consent-first website analytics and enquiries, run on DevHeal's own D-Move.
 *
 * Nothing is recorded until the visitor chooses "Accept" in the banner. The
 * choice is kept in this browser's local storage under
 * devheal-analytics-consent; "Decline" is remembered too, so the banner does
 * not return. No cookies, no advertising, no fingerprinting. See /privacy/.
 */
(function () {
  "use strict";
  var DMOVE = "https://dmove.devheallabs.com";
  var SITE_KEY = "mkPaxdZVJGUe2hs-8UwW5A4LIrGTCQ7WEK-X9xnMw3ThQ8IY";
  var STORE = "devheal-analytics-consent";
  var NOTICE_VERSION = "devheal-privacy-2026-11-05";
  var visitor = null;

  function choice() {
    try { return localStorage.getItem(STORE); } catch (e) { return null; }
  }
  function remember(value) {
    try { localStorage.setItem(STORE, value); } catch (e) {}
  }
  function consented() { return choice() === "granted"; }

  function start() {
    if (!window.DMoveVisitor || visitor) return;
    try {
      visitor = window.DMoveVisitor.init({
        endpoint: DMOVE + "/api/v1/visitor-intelligence",
        siteKey: SITE_KEY,
        analyticsConsent: consented
      });
    } catch (e) { return; }
    var slot = document.getElementById("dmove-visitor-widget");
    // The form loads its content from D-Move; if that fails the slot stays empty.
    if (slot) visitor.mountWidget("#dmove-visitor-widget", { noticeVersion: NOTICE_VERSION }).catch(function () {});
  }

  function banner() {
    if (choice() || document.getElementById("devheal-consent")) return;
    var box = document.createElement("div");
    box.id = "devheal-consent";
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Analytics choice");
    box.style.cssText = "position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:560px;" +
      "margin:0 auto;padding:16px 18px;border-radius:12px;background:#0f172a;color:#f8fafc;" +
      "box-shadow:0 10px 30px rgba(0,0,0,.25);font:14px/1.5 system-ui,-apple-system,Segoe UI,sans-serif";
    var text = document.createElement("p");
    text.style.margin = "0 0 12px";
    text.innerHTML = "May we record which pages and products you view, to improve this site and our " +
      "follow-up? No cookies or advertising. <a href=\"/privacy/#analytics\" style=\"color:#93c5fd\">Details</a>";
    var row = document.createElement("div");
    row.style.cssText = "display:flex;gap:8px;justify-content:flex-end";
    function button(label, primary, value) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = label;
      b.style.cssText = "padding:8px 14px;border-radius:8px;cursor:pointer;font:inherit;border:1px solid " +
        (primary ? "#3b82f6;background:#3b82f6;color:#fff" : "#475569;background:transparent;color:#f8fafc");
      b.addEventListener("click", function () {
        remember(value);
        box.remove();
        if (value === "granted" && visitor) visitor.track("page_view").catch(function () {});
      });
      return b;
    }
    row.appendChild(button("Decline", false, "denied"));
    row.appendChild(button("Accept", true, "granted"));
    box.appendChild(text);
    box.appendChild(row);
    document.body.appendChild(box);
  }

  // Lets the privacy page offer "change my choice".
  window.DevHealAnalytics = Object.freeze({
    reset: function () {
      try { localStorage.removeItem(STORE); } catch (e) {}
      banner();
    }
  });

  function boot() {
    var s = document.createElement("script");
    s.src = DMOVE + "/visitor-sdk.js";
    s.async = true;
    s.onload = start;
    document.head.appendChild(s);
    banner();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
