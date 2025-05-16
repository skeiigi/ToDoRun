function showLoader() {
    document.getElementById('loader').style.display = 'flex';
}
function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

function createDeferred() {
    let resolve, reject;
    const promise = new Promise((res, rej) => {
        resolve = res;
        reject = rej;
    });
    
    return {
        promise: promise,
        resolve: resolve,
        reject: reject,
        then: function(onResolve, onReject) {
            return promise.then(onResolve, onReject);
        },
        catch: function(onReject) {
            return promise.catch(onReject);
        },
        finally: function(onFinally) {
            return promise.finally(onFinally);
        }
    };
}

function taskOperation(operation, data = {}) {
    const deferred = createDeferred();
    
    showLoader();
    
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/ajax/task-operation/');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    
    xhr.onload = function() {
        if (xhr.status === 200) {
            try {
                const response = JSON.parse(xhr.responseText);
                if (response.status === 'success') {
                    deferred.resolve(response);
                } else {
                    deferred.reject(response);
                }
            } catch (e) {
                deferred.reject({
                    status: 'error',
                    message: 'Ошибка парсинга ответа сервера'
                });
            }
        } else {
            deferred.reject({
                status: 'error',
                message: 'Ошибка сервера: ' + xhr.status
            });
        }
    };
    
    xhr.onerror = function() {
        deferred.reject({
            status: 'error',
            message: 'Ошибка сети'
        });
    };
    
    xhr.send(JSON.stringify({
        operation: operation,
        ...data
    }));
    
    return {
        then: function(onResolve, onReject) {
            return deferred.then(onResolve, onReject).finally(hideLoader);
        },
        catch: function(onReject) {
            return deferred.catch(onReject).finally(hideLoader);
        },
        finally: function(onFinally) {
            return deferred.finally(onFinally).finally(hideLoader);
        }
    };
}

document.getElementById('task-create-form').addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const form = this;
    const formData = {
        title: form.querySelector('[name="title"]').value,
        descriptionn: form.querySelector('[name="descriptionn"]').value,
        operation: 'create'
    };
    
    const taskCreation = taskOperation('create', formData);
    
    taskCreation
        .then(function(response) {
            console.log('Задача успешно создана', response);
            document.getElementById('task-popup').style.display = 'none';

            form.reset();

            return updateTasksList();
        })
        .catch(function(error) {
            console.error('Ошибка при создании задачи', error);
            alert('Ошибка: ' + (error.message || 'Неизвестная ошибка'));
        })
        .finally(function() {
            console.log('Операция создания задачи завершена');
        });
});


function updateTasksList() {
    const deferred = createDeferred();
    
    fetch(window.location.href)
        .then(response => response.text())
        .then(text => {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = text;
            
            const newTasksContainer = tempDiv.querySelector('.task__cards-container');
            if (newTasksContainer) {
                const currentContainer = document.querySelector('.task__cards-container');
                if (currentContainer) {
                    currentContainer.innerHTML = newTasksContainer.innerHTML;
                } else {
                    document.querySelector('.task__main').innerHTML = tempDiv.querySelector('.task__main').innerHTML;
                }
                deferred.resolve('Список задач обновлен');
            } else {
                deferred.reject('Не удалось найти контейнер задач');
            }
        })
        .catch(error => {
            console.error('Ошибка при обновлении списка задач:', error);
            window.location.reload();
            deferred.reject(error);
        });
    
    return deferred;
}

function multipleOperationsExample() {
    const op1 = taskOperation('dummy_operation_1');
    const op2 = taskOperation('dummy_operation_2');

    Promise.all([op1, op2])
        .then(function(results) {
            console.log('Все операции завершены успешно', results);
        })
        .catch(function(error) {
            console.log('Одна из операций завершилась ошибкой', error);
        });
}

document.addEventListener('change', function(e) {
    if (e.target.classList.contains('task__status-checkbox')) {
        const taskId = e.target.form.querySelector('input[name="task_id"]').value;
        const isChecked = e.target.checked;
        
        taskOperation('toggle_status', {task_id: taskId})
            .then(function(response) {
                const taskCard = e.target.closest('.task__card');
                if (response.new_status) {
                    taskCard.classList.add('task__completed');
                } else {
                    taskCard.classList.remove('task__completed');
                }
            })
            .catch(function(error) {
                console.error('Ошибка:', error);
                e.target.checked = !isChecked;
                alert('Произошла ошибка при изменении статуса задачи');
            });
    }
});
