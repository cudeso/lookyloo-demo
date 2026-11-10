// Uses the CDN copy of jQuery on purpose, so the capture shows the library loading and then making a request.
$(function () {
  $.getJSON("api/most-read.json", function (data) {
    var list = $("#most-read");
    $.each(data.articles, function (index, article) {
      list.append($("<li>").append($("<a>").attr("href", article.url).text(article.title)));
    });
  });
});
