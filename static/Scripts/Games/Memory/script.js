document.addEventListener("DOMContentLoaded", function () {
    const cardImages = document.querySelectorAll(".card-image");
    cardImages.forEach(function (image, index) {
      image.id = "card-image-" + index;
    });
  });

  const cards = document.getElementsByClassName("card");
  const clickCounter = document.getElementById("click-counter");
  let toggledCardsArray = [];
  let move = 0;
  let winCount = 0;
  let startTime = Date.now();

  function displayTime() {
    let currentTime = Date.now();
    let elapsedTime = Math.floor((currentTime - startTime) / 1000);
    let minutes = Math.floor(elapsedTime / 60);
    let seconds = elapsedTime % 60;
    document.getElementById("timer").textContent = `Tijd: ${
      minutes < 10 ? "0" : ""
    }${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  }

  setInterval(displayTime, 1000);

  for (let i = 0; i < cards.length; i++) {
    cards[i].addEventListener("click", handleCardClick);
  }

  function handleCardClick() {
    // Controleren of de kaart al is omgedraaid
    if (!this.classList.contains("toggled")) {
      this.classList.add("toggled");
      toggledCardsArray.push(this);
      let thisImgSrc = this.querySelector(".card-image").src;
      let previousImgSrc =
        toggledCardsArray[toggledCardsArray.length - 2].querySelector(
          ".card-image"
        ).src;

      if (thisImgSrc !== previousImgSrc) {
        toggledCardsArray.forEach(function (el) {
          setTimeout(() => {
            el.classList.remove("toggled");
          }, 1000);
        });
        toggledCardsArray.length = 0;
        move++;
      } else {
        if (toggledCardsArray.length === 2) {
          toggledCardsArray.length = 0;
          move++;
          winCount++;
        }
      }
      updateMoveCounter();
      const totalPairs = document.querySelectorAll(".card").length / 2;

      if (winCount === totalPairs) {
        handleGameEnd();
      }
    }
  }

  function updateMoveCounter() {
    clickCounter.textContent = `Combinaties: ${move}`;
  }

  function handleGameEnd() {
    let endTime = Date.now();
    let gameTimeInSeconds = Math.floor((endTime - startTime) / 1000);
    setTimeout(function () {
      window.location.href = `/Memory/Einde?moves=${move}&time=${gameTimeInSeconds}`;
    }, 1000);
  }