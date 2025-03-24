document.addEventListener("DOMContentLoaded", () => {
  const articles = document.querySelectorAll(".hero__container-img a article");

  articles.forEach((article) => {
    article.addEventListener("mouseenter", () => {
      articles.forEach((otherArticle) => {
        if (otherArticle !== article) {
          otherArticle.style.transform = "scaleX(0.9)";
        }
      });
    });

    article.addEventListener("mouseleave", () => {
      articles.forEach((otherArticle) => {
        otherArticle.style.transform = "scaleX(1)";
      });
    });
  });
});
