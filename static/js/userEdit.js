$(document).ready(function () {
  $("#rut").keyup(() => {
    const rut = $("#rut").val();

    if (
      rut.length === 0 ||
      rut.length < 9 ||
      (rut.length > 9 && rut.length < 12)
    ) {
      $("#rut").addClass("is-invalid");
      $("#save").prop("disabled", true);
      return;
    }

    $("#rut").removeClass("is-invalid");
    $("#save").prop("disabled", false);

    //Format rut
    const rutFormated = rut.replace(/\./g, "").replace(/\-/g, "");
    const rutArray = rutFormated.split("");
    let rutFormatedFinal = "";
    let count = 0;
    for (let i = 0; i < rutArray.length; i++) {
      if (count === 2 || count === 5) {
        rutFormatedFinal += ".";
      }
      if (count === 8) {
        rutFormatedFinal += "-";
        const allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "k"];
        if (!allowed.includes(rutArray[i].toLowerCase())) {
          break;
        }
      }
      rutFormatedFinal += rutArray[i];
      count++;
    }
    $("#rut").val(rutFormatedFinal);
  });
});
