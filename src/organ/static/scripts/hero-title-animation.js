document.addEventListener("DOMContentLoaded", function() {
  const text = "To Do Run";
  const typedTextElement = document.getElementById("typed-text");
  let i = 0;

  function typeWriter() {
    if (i < text.length) {
      typedTextElement.innerHTML += text.charAt(i);
      i++;
      setTimeout(typeWriter, 250);
    }
  }

  typeWriter();
});
