document.getElementById("login-form").addEventListener("submit", function (event) {
  event.preventDefault();
  document.getElementById("passphrase").value = "";
  document.getElementById("login-message").hidden = false;
});
