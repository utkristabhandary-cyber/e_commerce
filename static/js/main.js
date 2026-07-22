// Prevent double-submit on forms
document.querySelectorAll("form").forEach(form => {
  form.addEventListener("submit", () => {
    const btn = form.querySelector("button[type=submit]");
    if (btn) { btn.disabled = true; btn.textContent = "Please wait…"; }
  });
});
