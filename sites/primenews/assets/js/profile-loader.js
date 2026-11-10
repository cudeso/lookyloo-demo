// Byte-identical on NewsCorp and PrimeNews. Both load profiler.js from the NewsCorp host, which links the two sites in Lookyloo.
// The host is derived from the current one, so this works on localhost and on the deployment domain.
var profiler = document.createElement("script");
profiler.src = "//" + location.host.replace(/^[^.]+\./, "newscorp.") + "/assets/js/profiler.js";
document.head.appendChild(profiler);
