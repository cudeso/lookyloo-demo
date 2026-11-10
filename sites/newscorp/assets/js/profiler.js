// Sends one tracking beacon to the NewsCorp host. The account ID is a fixed demo value, the same on every site that loads this file.
var beacon = new URL("/api/pixel.gif", document.currentScript.src);
beacon.searchParams.set("account", "NLD-20431");
beacon.searchParams.set("page", location.pathname);
new Image().src = beacon.href;
