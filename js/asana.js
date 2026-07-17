document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('asanaOverlay');
    const petIdInput = document.getElementById('asanaPetId');
    const petNameEl = document.getElementById('asanaPetName');

    window.openAsanaModal = function (petId, petName) {
        if (petIdInput) petIdInput.value = petId;
        if (petNameEl) petNameEl.textContent = petName;
        overlay.classList.add('active');
    };

    document.getElementById('asanaClose').addEventListener('click', () => overlay.classList.remove('active'));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.classList.remove('active'); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') overlay.classList.remove('active'); });

    document.getElementById('asanaSubmit').addEventListener('click', async () => {
        const nameInput = document.getElementById('asanaUserName');
        const emailInput = document.getElementById('asanaUserEmail');
        const phoneInput = document.getElementById('asanaUserPhone');
        const messageInput = document.getElementById('asanaMessage');

        if (!nameInput.value.trim()) { nameInput.focus(); return; }

        const submitBtn = document.getElementById('asanaSubmit');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';

        try {
            const formData = new FormData();
            formData.append('pet_id', petIdInput.value);
            formData.append('name', nameInput.value.trim());
            formData.append('email', emailInput.value.trim());
            formData.append('phone', phoneInput.value.trim());
            formData.append('message', messageInput.value.trim());

            const resp = await fetch('/api/asana/task', { method: 'POST', body: formData });

            if (resp.ok) {
                overlay.classList.remove('active');
                alert('Задача создана в Asana!');
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
