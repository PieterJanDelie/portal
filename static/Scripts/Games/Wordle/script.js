
document.addEventListener("DOMContentLoaded", () => {
  let guessedWords = [[]];
  let availableSpace = 1;

  let word = document.getElementById("wordValue").value;
  document.getElementById("board").style.gridTemplateColumns =
    "repeat(" + word.length + ", 1fr)";
  console.log("Woord = " + word);
  let guessedWordCount = 0;

  const keys = document.querySelectorAll(".keyboard-row button");

  function getCurrentWordArr() {
    const numberOfGuessedWords = guessedWords.length;
    return guessedWords[numberOfGuessedWords - 1];
  }

  function updateGuessedWords(letter) {
    const currentWordArr = getCurrentWordArr();

    if (currentWordArr && currentWordArr.length < word.length) {
      currentWordArr.push(letter);

      const availableSpaceEl = document.getElementById(
        String(availableSpace)
      );

      availableSpace = availableSpace + 1;
      availableSpaceEl.textContent = letter;
    }
  }

  function getTileColor(letter, index) {
    const isCorrectLetter = word.includes(letter);

    if (!isCorrectLetter) {
      return "rgb(128, 128, 128)";
    }

    const letterInThatPosition = word.charAt(index);
    const isCorrectPosition = letter === letterInThatPosition;

    if (isCorrectPosition) {
      return "rgb(83, 141, 78)";
    }

    return "rgb(181, 159, 59)";
  }

  function handleSubmitWord() {
    const currentWordArr = getCurrentWordArr();
    if (currentWordArr.length === word.length) {
      const currentWord = currentWordArr.join("");

      const firstLetterId = guessedWordCount * word.length + 1;
      const interval = 200;
      const yellowLetters = [];
      currentWordArr.forEach((letter, index) => {
        setTimeout(() => {
          const tileColor = getTileColor(letter, index);

          const letterId = firstLetterId + index;
          const letterEl = document.getElementById(letterId);
          letterEl.classList.add("animate__flipInX");
          letterEl.style = `background-color:${tileColor};border-color:${tileColor}`;
        }, interval * index);
      });

      guessedWordCount += 1;

      if (currentWord === word) {
        setTimeout(() => {
          window.location.href = "/Wordle/Einde/Geraden";
        }, 200 * (word.length + 1));
      }

      if (guessedWords.length === 6) {
        setTimeout(() => {
          window.location.href = "/Wordle/Einde/NGeraden";
        }, 200 * (word.length + 1));
      }

      guessedWords.push([]);
    }
  }

  function createSquares() {
    const gameBoard = document.getElementById("board");

    for (let index = 0; index < word.length * 6; index++) {
      let square = document.createElement("div");
      square.classList.add("square");
      square.classList.add("animate__animated");
      square.setAttribute("id", index + 1);
      gameBoard.appendChild(square);
    }
  }

  function handleDeleteLetter() {
    const currentWordArr = getCurrentWordArr();
    const removedLetter = currentWordArr.pop();

    guessedWords[guessedWords.length - 1] = currentWordArr;

    const lastLetterEl = document.getElementById(
      String(availableSpace - 1)
    );

    lastLetterEl.textContent = "";
    availableSpace = availableSpace - 1;
  }

  for (let i = 0; i < keys.length; i++) {
    keys[i].onclick = ({ target }) => {
      const letter = target.getAttribute("data-key");

      if (letter === "enter") {
        handleSubmitWord();
        return;
      }

      if (letter === "del") {
        handleDeleteLetter();
        return;
      }

      updateGuessedWords(letter);
    };
  }

  createSquares();
});