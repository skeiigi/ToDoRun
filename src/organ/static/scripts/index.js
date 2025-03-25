const articles = document.querySelectorAll(".hero__container-img a article");
const text = "To Do Run";
const typedTextElement = document.getElementById("typed-text");
const deleteAccountButton = document.getElementById('deleteAccountButton');
const customPopup = document.getElementById('customPopup');
const cancelButton = document.getElementById('cancelButton');

articles.forEach((article) => {
  article.addEventListener("mouseenter", () => {
    articles.forEach((otherArticle) => {
      if (otherArticle !== article)
        otherArticle.style.transform = "scaleX(0.9)"
    });
  });

  article.addEventListener("mouseleave", () => {
    articles.forEach(
      (otherArticle) => otherArticle.style.transform = "scaleX(1)");
  });
});

if (typedTextElement) {
  let i = 0;

  function typeWriter() {
    if (i < text.length) {
      typedTextElement.innerHTML += text.charAt(i);
      i++;
      setTimeout(typeWriter, 250);
    }
  }

  typeWriter();
}

if (deleteAccountButton) {
  deleteAccountButton.addEventListener('click', () =>
    customPopup.style.display = 'flex');
}

if (cancelButton) {
  cancelButton.addEventListener('click', () =>
    customPopup.style.display = 'none');
}

if (customPopup) {
  window.addEventListener('click', (event) => {
    if (event.target === customPopup)
      customPopup.style.display = 'none';
  });
}
