export function initPopupManager() {
  const deleteAccountButton = document.getElementById('deleteAccountButton');
  const customPopup = document.getElementById('customPopup');
  const cancelButton = document.getElementById('cancelButton');

  if (deleteAccountButton && customPopup) {
    deleteAccountButton.addEventListener('click', () => 
      customPopup.style.display = 'flex');
  }

  if (cancelButton && customPopup) {
    cancelButton.addEventListener('click', () => 
      customPopup.style.display = 'none');
  }

  if (customPopup) {
    window.addEventListener('click', (event) => {
      if (event.target === customPopup) 
        customPopup.style.display = 'none';
    });
  }
}
