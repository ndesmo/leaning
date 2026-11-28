// Proofs by Claude: shared page script. Loaded with `defer` after KaTeX and its auto-render.
// 1. Typesets \( inline \) and \[ display \] maths with KaTeX.
// 2. Adds the light/dark toggle. Dark is the default; the choice is remembered per browser.
(function () {
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false }
      ],
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
      throwOnError: false
    });
  }

  var root = document.documentElement;
  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "theme-toggle";
  function label() {
    var light = root.getAttribute("data-theme") === "light";
    btn.textContent = light ? "Dark" : "Light";
    btn.setAttribute("aria-label", light ? "Switch to dark theme" : "Switch to light theme");
  }
  btn.addEventListener("click", function () {
    var light = root.getAttribute("data-theme") === "light";
    if (light) root.removeAttribute("data-theme"); else root.setAttribute("data-theme", "light");
    try { localStorage.setItem("theme", light ? "dark" : "light"); } catch (e) {}
    label();
  });
  label();
  document.body.appendChild(btn);
})();
