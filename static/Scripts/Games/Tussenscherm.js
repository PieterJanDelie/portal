document.addEventListener("DOMContentLoaded", () => {
  var titleElement = document.getElementById("screentitle");
  var titleText = titleElement.innerHTML.trim().toLowerCase();

  if (titleText.includes("correct")) {
    titleElement.classList.add("correct");
  } else if (titleText.includes("fout") || titleText.includes("incorrect")) {
    titleElement.classList.add("incorrect");
  }
});
