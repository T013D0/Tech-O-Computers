$(document).ready(function () {
  $(".avatar").change(function () {
    displayImage();
  });
  $("#type").change(function () {
    if (["notebook", "allinone"].includes($("#type").val())) {
      $("#screenSelect").show();
      $("#screen").attr("disabled", false);
    } else {
      $("#screenSelect").hide();
      $("#screen").attr("disabled", true);
    }
  });
});

function displayImage() {
  const input = document.getElementById("avatar");
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (event) {
      const imageDataUrl = event.target.result;
      updateImageSrc(imageDataUrl);
    };
    reader.onerror = function (error) {
      console.error("Error reading the file:", error);
    };
    reader.readAsDataURL(file);
  }
}

function updateImageSrc(src) {
  const uploadedImage = document.getElementById("avatar-updated");
  uploadedImage.src = src;
}
