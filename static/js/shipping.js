$(document).ready(function () {
  const url =
    "https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=XXXXXXXXXXXX&longitude=XXXXXXXXXXXX&localityLanguage=es";

  $.get(url, function (data) {
    const region = data.principalSubdivision;
    const city = data.locality;

    $("#state").val(region);
    $("#city").val(city);
    initMap({ latitude: data.latitude, longitude: data.longitude });
  });

  /*$("#address").keyup(function () {
    const address = $(this).val();

    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${address};key=AIzaSyA5D3ZY9Iq_gVi3hJUV4Ble5Sxm5Lad7Jw`;
    $.get(url, function (data) {
      console.log(data);
      initMap({ latitude: data.latitude, longitude: data.longitude });
    });
  });*/   
});

let map;

async function initMap({ latitude, longitude } = {}) {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: latitude, lng: longitude },
    zoom: 12,
  });
}
