function iniciarMap() {
  var locations = [
      {lat: -34.5539994, lng: -58.4532738},
      {lat: -34.60360002009423, lng: -58.41083774766596},
      {lat: -34.62233139510712, lng:-58.79333497246394},
      {lat: -34.61329008806869, lng:-58.428039561110815},
      {lat: -34.543752168574756, lng: -58.48915101036944}
  ];

  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
          var userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
          };

          locations.push(userLocation);

          var map = new google.maps.Map(document.getElementById('map'), {
              zoom: 10,
              center: userLocation
          });

          for (var i = 0; i < locations.length; i++) {
              var marker = new google.maps.Marker({
                  position: locations[i],
                  map: map
              });
          }
      }, function(error) {
          // Manejo de errores de geolocalización
          console.error('Error al obtener la ubicación: ', error);

          // Mapa sin ubicación propia
          var map = new google.maps.Map(document.getElementById('map'), {
              zoom: 10,
              center: locations[0]
          });

          for (var i = 0; i < locations.length; i++) {
              var marker = new google.maps.Marker({
                  position: locations[i],
                  map: map
              });
          }
      });
    } else {
      // El navegador no soporta geolocalización
      console.error('Geolocalización no soportada por el navegador');

      // Mapa sin ubicación propia
      var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 10,
          center: locations[0]
      });

      for (var i = 0; i < locations.length; i++) {
          var marker = new google.maps.Marker({
              position: locations[i],
              map: map
          });
      }
  }
}