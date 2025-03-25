export function initTypeWriterEffect() {
  const typedTextElement = document.getElementById("typed-text");
  const text = "To Do Run";

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
}
