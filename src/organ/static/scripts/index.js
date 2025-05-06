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

// if (typedTextElement) {
//   let i = 0;

//   function typeWriter() {
//     if (i < text.length) {
//       typedTextElement.innerHTML += text.charAt(i);
//       i++;
//       setTimeout(typeWriter, 250);
//     }
//   }

//   typeWriter();
// }

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

if (window.location.pathname !== '/') {
  document.querySelector('.content').style.display = 'block';
  document.querySelector('.content').style.opacity = '1';
}

// preloader
if (window.location.pathname === '/') {
  document.addEventListener('DOMContentLoaded', function() {
    const preloader = document.getElementById('preloader');
    const content = document.querySelector('.content');
    const progress = document.getElementById('progress');
    const loadingText = document.querySelector('.loading-text');

    let width = 0;
    const interval = setInterval(() => {
      if (width >= 100) {
        clearInterval(interval);
        loadingText.textContent = "READY";

        setTimeout(() => {
          preloader.classList.add('preloader-done');
          content.style.display = 'block';
          void content.offsetWidth;
          content.style.opacity = '1';

          setTimeout(() => {
            preloader.style.display = 'none';

            // 👉 Запуск печати текста только после скрытия прелоадера
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

          }, 800);
        }, 600);
      } else {
        width += Math.floor(Math.random() * 5) + 1;
        width = Math.min(width, 100);
        progress.style.width = width + '%';

        if (width > 80) {
          loadingText.textContent = "ALMOST THERE";
        } else if (width > 50) {
          loadingText.textContent = "LOADING ASSETS";
        }
      }
    }, 50);
  });
}

window.addEventListener('load', function() {
});
