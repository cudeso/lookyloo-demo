// The IP lookup is a real cross-origin request, so the capture shows the page contacting a third-party service.
var connection = document.getElementById("connection");

function showField(name, value) {
  connection.querySelector('[data-field="' + name + '"]').textContent = value;
}

showField("browser", navigator.userAgent);
showField("language", navigator.language);
showField("screen", screen.width + " x " + screen.height);
showField("timezone", Intl.DateTimeFormat().resolvedOptions().timeZone);

fetch("https://ipinfo.io/json")
  .then(function (response) {
    if (!response.ok) {
      throw new Error("IP lookup returned " + response.status);
    }
    return response.json();
  })
  .then(function (info) {
    showField("ip", info.ip);
    showField("network", info.org);
    showField("country", info.country);
  })
  .catch(function () {
    showField("ip", "lookup failed");
  });
