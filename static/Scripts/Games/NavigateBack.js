var timer;

function navigateToGameCenter() {
  window.location.href = "/GameCenter";
}

function resetTimer() {
  var popup = document.getElementById("alert-box");
  popup.style.display = "none";

  clearTimeout(timer);

  timer = setTimeout(startAlertTimer, 20000);
}

function startAlertTimer() {
  var popup = document.getElementById("alert-box");
  popup.style.display = "block";

  timer = setTimeout(navigateToGameCenter, 7500);
}

window.onload = function () {
  resetTimer();
};
