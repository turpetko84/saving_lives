document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('jiraOverlay');
    const petIdInput = document.getElementById('jiraPetId');
    const petNameEl = document.getElementById('jiraPetName');

    window.openJiraModal = function (petId, petName) {
        if (petIdInput) petIdInput.value = petId;
        if (petNameEl) petNameEl.textContent = petName;
        overlay.classList.add('active');
    };

    document.getElementById('jiraClose').addEventListener('click', () => overlay.classList.remove('active'));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.classList.remove('active'); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') overlay.classList.remove('active'); });

    document.getElementById('jiraSubmit').addEventListener('click', async () => {
        const nameInput = document.getElementById('jiraUserName');
        const emailInput = document.getElementById('jiraUserEmail');
        const phoneInput = document.getElementById('jiraUserPhone');
        const messageInput = document.getElementById('jiraMessage');

        if (!nameInput.value.trim()) { nameInput.focus(); return; }

        const submitBtn = document.getElementById('jiraSubmit');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';

        try {
            const formData = new FormData();
            formData.append('pet_id', petIdInput.value);
            formData.append('name', nameInput.value.trim());
            formData.append('email', emailInput.value.trim());
            formData.append('phone', phoneInput.value.trim());
            formData.append('message', messageInput.value.trim());

            const resp = await fetch('/api/jira/task', { method: 'POST', body: formData });

            if (resp.ok) {
                overlay.classList.remove('active');
                alert('Задача создана в Jira!');
                nameInput.value = '';
                emailInput.value = '';
                phoneInput.value = '';
                messageInput.value = '';
            } else {
                const err = await resp.json();
                alert('Ошибка: ' + (err.detail || 'Не удалось создать задачу'));
            }
        } catch (e) {
            alert('Ошибка сети. Попробуйте ещё раз.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Отправить';
        }
    });
});
