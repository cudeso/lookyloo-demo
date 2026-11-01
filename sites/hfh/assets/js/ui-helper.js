// Shared by the market, hfh and newscorp demo sites. Keep the copies byte-identical: their hashes link the sites in Lookyloo.
document.querySelectorAll(".menu-toggle").forEach(function (button) {
  var menu = document.getElementById(button.getAttribute("aria-controls"));
  button.addEventListener("click", function () {
    var open = button.getAttribute("aria-expanded") !== "true";
    button.setAttribute("aria-expanded", String(open));
    menu.classList.toggle("is-open", open);
  });
});

// Requested after the homepage has set the site's cookie, so the capture shows the cookie being sent back.
var sessionNotice = document.querySelector("[data-session]");
fetch("/api/session.json")
  .then(function (response) { return response.json(); })
  .then(function (session) { sessionNotice.textContent = session.message; });
