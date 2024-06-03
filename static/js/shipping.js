$(document).ready(function () {
  const url =
    "https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=XXXXXXXXXXXX&longitude=XXXXXXXXXXXX&localityLanguage=es";

  $.get(url, function (data, status) {
    console.log(data);
    console.log(status);
  });
});
