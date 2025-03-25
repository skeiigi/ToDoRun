const popup = document.getElementById('task-popup');
const openButtons = document.querySelectorAll('#open-task-popup, #open-task-popup-2');
const closeButton = document.getElementById('close-task-popup');

openButtons.forEach(button => {
  button.addEventListener('click', function(e) {
    e.preventDefault();
    popup.style.display = 'flex';
  });
});

closeButton.addEventListener('click', function() {
  popup.style.display = 'none';
});

window.addEventListener('click', function(e) {
  if (e.target === popup) {
    popup.style.display = 'none';
  }
});