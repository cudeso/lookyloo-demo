// Stored sample results. The demo never contacts the monitored sites.
var sampleResults = {
  shop: { title: "Web shop checkout page", status: "Up · 200 OK", ok: true, locations: "4 of 4", dns: "12 ms", tls: "38 ms", ttfb: "164 ms", cert: "61 days" },
  api: { title: "Booking API health endpoint", status: "Up · 200 OK", ok: true, locations: "4 of 4", dns: "9 ms", tls: "31 ms", ttfb: "88 ms", cert: "212 days" },
  portal: { title: "Customer portal login page", status: "Slow · 200 OK", ok: false, locations: "3 of 4", dns: "14 ms", tls: "41 ms", ttfb: "1,920 ms", cert: "9 days" }
};

document.getElementById("sample-form").addEventListener("submit", function (event) {
  event.preventDefault();
  var result = sampleResults[document.getElementById("sample-monitor").value];
  var status = document.getElementById("result-status");
  document.getElementById("result-title").textContent = result.title;
  status.textContent = result.status;
  status.className = result.ok ? "status-ok" : "status-warn";
  document.getElementById("result-locations").textContent = result.locations;
  document.getElementById("result-dns").textContent = result.dns;
  document.getElementById("result-tls").textContent = result.tls;
  document.getElementById("result-ttfb").textContent = result.ttfb;
  document.getElementById("result-cert").textContent = result.cert;
});

document.getElementById("contact-form").addEventListener("submit", function (event) {
  event.preventDefault();
  event.target.reset();
  document.getElementById("contact-message").hidden = false;
});
