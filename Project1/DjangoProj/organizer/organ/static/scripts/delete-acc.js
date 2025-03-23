document.addEventListener('DOMContentLoaded', function () {
  const deleteAccountButton = document.getElementById('deleteAccountButton');
  const customPopup = document.getElementById('customPopup');
  const cancelButton = document.getElementById('cancelButton');

  if (deleteAccountButton) {
    deleteAccountButton.addEventListener('click', () => {
        customPopup.style.display = 'flex';
    });
  }

  if (cancelButton) {
    cancelButton.addEventListener('click', () => {
        customPopup.style.display = 'none';
    });
  }

  if (customPopup) {
      window.addEventListener('click', (event) => {
        if (event.target === customPopup) {
            customPopup.style.display = 'none';
        }
      });
  }
});
