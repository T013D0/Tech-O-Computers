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

addEventListener("DOMContentLoaded", (event) => {
  const password = document.getElementById("password1");
  const password_2 = document.getElementById("password2");
  const passwordAlert = document.getElementById("password-alert");
  const requirements = document.querySelectorAll(".requirements");
  const leng = document.querySelector(".leng");
  const bigLetter = document.querySelector(".big-letter");
  const num = document.querySelector(".num");
  const passwordAlertMatch = document.getElementById("password-alert-match");
  const match = document.querySelector(".match");

  requirements.forEach((element) => element.classList.add("wrong"));

  password.addEventListener("focus", () => {
    passwordAlert.classList.remove("d-none");
    if (!password.classList.contains("is-valid")) {
      password.classList.add("is-invalid");
    }
  });

  password.addEventListener("input", () => {
    const value = password.value;
    const isLengthValid = value.length >= 8;
    const hasUpperCase = /[A-Z]/.test(value);
    const hasNumber = /\d/.test(value);

    leng.classList.toggle("good", isLengthValid);
    leng.classList.toggle("wrong", !isLengthValid);
    bigLetter.classList.toggle("good", hasUpperCase);
    bigLetter.classList.toggle("wrong", !hasUpperCase);
    num.classList.toggle("good", hasNumber);
    num.classList.toggle("wrong", !hasNumber);

    const isPasswordValid = isLengthValid && hasUpperCase && hasNumber;

    if (isPasswordValid) {
      password.classList.remove("is-invalid");
      password.classList.add("is-valid");

      requirements.forEach((element) => {
        element.classList.remove("wrong");
        element.classList.add("good");
      });

      passwordAlert.classList.remove("alert-warning");
      passwordAlert.classList.add("alert-success");
    } else {
      password.classList.remove("is-valid");
      password.classList.add("is-invalid");

      passwordAlert.classList.add("alert-warning");
      passwordAlert.classList.remove("alert-success");
    }
  });

  password.addEventListener("blur", () => {
    passwordAlert.classList.add("d-none");
  });

  password_2.addEventListener("focus", () => {
    passwordAlertMatch.classList.remove("d-none");
    if (password_2.value === password.value) {
      match.classList.remove("wrong");
      match.classList.add("good");
    } else {
      match.classList.remove("good");
      match.classList.add("wrong");
    }
    if (!password_2.classList.contains("is-valid")) {
      password_2.classList.add("is-invalid");
    }
  });

  password_2.addEventListener("input", () => {
    if (password_2.value === password.value) {
      password_2.classList.remove("is-invalid");
      password_2.classList.add("is-valid");
      match.classList.remove("wrong");
      match.classList.add("good");
    } else {
      password_2.classList.remove("is-valid");
      password_2.classList.add("is-invalid");
      match.classList.remove("good");
      match.classList.add("wrong");
    }
  });

  password_2.addEventListener("blur", () => {
    passwordAlertMatch.classList.add("d-none");
  });
});
