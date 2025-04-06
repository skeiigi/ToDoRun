async function deleteAllTasks(e) {
  e.preventDefault();

  const deleteAllButton = document.getElementById('delete-all-tasks');
  if (!deleteAllButton) return;

  const csrfToken = deleteAllButton.dataset.csrfToken;
  const deleteUrl = deleteAllButton.dataset.deleteUrl;

  if (!confirm('Вы уверены, что хотите удалить ВСЕ задачи?')) return;

  try {
    const response = await fetch(deleteUrl, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken ,
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      alert('Все задачи удалены!');
      location.reload();
    } else {
      alert('Ошибка при удалении задач.');
    }
  } catch (error) {
    console.error('Ошибка:', error);
  }
}

const deleteAllButton = document.getElementById('delete-all-tasks');
const noTasksText = document.querySelector('.task__no-tasks'); 
if (!noTasksText) {
  deleteAllButton.addEventListener('click', deleteAllTasks);
}
