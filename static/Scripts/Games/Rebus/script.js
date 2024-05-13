
let word = document.getElementById("wordValue").value;
word = word.trim().toLowerCase();
const keyboardButtons = document.querySelectorAll("button");
keyboardButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const letter = button.dataset.key;
    const currentText = document.getElementById("woordgok").textContent;

    var newText = currentText;
    if (letter === "enter") {
      if (currentText === word) {
        window.location.href = "/Rebus/Einde/Geraden";
      } else {
        window.location.href = "/Rebus/Einde/NGeraden";
      }
    } else if (letter === "del") {
      newText = currentText.slice(0, -1);
    } else {
      newText += letter;
    }

    document.getElementById("woordgok").textContent = newText;
  });
});