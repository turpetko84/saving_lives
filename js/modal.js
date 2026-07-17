document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('modalOverlay');
    const messageField = document.getElementById('modalMessage');
    const petNameEl = document.getElementById('modalPetName');
    const petIdInput = document.getElementById('modalPetId');

    window.openModal = function (name, petId) {
        if (name && petNameEl) petNameEl.textContent = name;
        if (petIdInput) petIdInput.value = petId || '';
        messageField.value = '';
        overlay.classList.add('active');
    };

    document.getElementById('modalClose').addEventListener('click', () => overlay.classList.remove('active'));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.classList.remove('active'); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') overlay.classList.remove('active'); });

    document.getElementById('modalSubmit').addEventListener('click', async () => {
        const petName = petNameEl ? petNameEl.textContent.trim() : '';
        const petId = petIdInput ? petIdInput.value : '';
        const nameInput = document.getElementById('modalUserName');
        const emailInput = document.getElementById('modalUserEmail');
        const phoneInput = document.getElementById('modalUserPhone');
        const message = messageField.value.trim();

        if (!nameInput || !nameInput.value.trim()) {
            if (nameInput) nameInput.focus();
            return;
        }
        if (!message) {
            messageField.focus();
            return;
        }

        const submitBtn = document.getElementById('modalSubmit');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';

        try {
            const resp = await fetch('/api/applications', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    pet_id: parseInt(petId) || 0,
                    name: nameInput.value.trim(),
                    email: emailInput ? emailInput.value.trim() : '',
                    phone: phoneInput ? phoneInput.value.trim() : '',
                    message: message,
                }),
            });

            if (resp.ok) {
                overlay.classList.remove('active');
                alert('Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время.');
                nameInput.value = '';
                if (emailInput) emailInput.value = '';
                if (phoneInput) phoneInput.value = '';
                messageField.value = '';
            } else {
                alert('Ошибка при отправке. Попробуйте ещё раз.');
            }
        } catch (err) {
            alert('Ошибка сети. Проверьте подключение и попробуйте ещё раз.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Отправить';
        }
    });
});
