const keyboardButtons = document.querySelectorAll("#keyboard-container button");
const textarea = document.getElementById("suggesties");

keyboardButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const letter = button.dataset.key;
    console.log(letter);

    if (letter === "del") {
      textarea.value = textarea.value.slice(0, -1);
    } else if (letter === "enter") {
      document.getElementById("feedbackform").submit();
    } else {
      textarea.value += letter;
    }
  });
});
