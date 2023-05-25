document.addEventListener('DOMContentLoaded', function() {
    var icons = document.querySelectorAll('.icon');

    icons.forEach(function(icon) {
        icon.addEventListener('click', function() {
            var popup = this.querySelector('.popup');
            popup.style.display = 'block';

            setTimeout(function() {
                popup.style.display = 'none';
            }, 2000);
        });
    });
});
