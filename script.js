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

Function
redirectToRandomSection() 
{
    var sections = [ 'Peliculas.html','Series.html', 'Documentales.html'];
    var randomindex = Math.floor(Math.random() * sections.length);
    var randomSection = sections[randomindex];
    window.location.href = randomSection;}
