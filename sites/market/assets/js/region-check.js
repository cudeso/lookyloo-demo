// Loaded without defer so it runs before the page renders. Only the browser knows its time zone, so the page asks the server for the refusal.
if (Intl.DateTimeFormat().resolvedOptions().timeZone === "Europe/Minsk") {
  location.replace("/blocked");
}
