document.addEventListener('DOMContentLoaded', function () {
    const toasts = document.querySelectorAll('.custom-toast');

    toasts.forEach(toast => {
        // Automatically close after 7 seconds
        setTimeout(() => {
            const bsToast = new bootstrap.Alert(toast);
            bsToast.close();
        }, 7000);
    });
});
