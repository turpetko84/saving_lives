document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('modalOverlay');
    const messageField = document.getElementById('modalMessage');
    const petNameEl = document.getElementById('modalPetName');

    window.openModal = function (name) {
        if (name && petNameEl) petNameEl.textContent = name;
        messageField.value = '';
        overlay.classList.add('active');
    };

    document.getElementById('modalClose').addEventListener('click', () => overlay.classList.remove('active'));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.classList.remove('active'); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') overlay.classList.remove('active'); });

    document.getElementById('modalSubmit').addEventListener('click', () => {
        const petName = petNameEl ? petNameEl.textContent.trim() : '';
        const message = messageField.value.trim();
        if (!message) { messageField.focus(); return; }
        const subject = encodeURIComponent('Хочу забрать ' + petName);
        const body = encodeURIComponent('Питомец: ' + petName + '\n\n' + message);
        window.location.href = 'mailto:turpetko84@gmail.ru?subject=' + subject + '&body=' + body;
    });
});
