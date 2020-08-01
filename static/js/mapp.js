mapboxgl.accessToken = 'pk.eyJ1IjoicHVueWF4MjAxIiwiYSI6ImNrMDljaW95ejA2dGUzbXF2bGhmbjNwaXcifQ.AIJO_GYOgGHa-rF7T6hEkA';


function placeLocator(long,lat){

    console.log("-"+lat+" "+long)
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/dark-v10',
        center: [lat,long],
        zoom: 13
        });

        const gl=new mapboxgl.GeolocateControl({
            positionOptions: {
            enableHighAccuracy: true
            },
            trackUserLocation: true,
            });
        map.addControl(gl);

        setTimeout(function() {
            $(".mapboxgl-ctrl-geolocate").click();
        },500);


    map.addControl(new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,

        // limit results to Australia
        countries: 'in',

        // further limit results to the geographic bounds representing the region of
        // Curr Region
        bbox: [lat-5, long-5, lat+5, long+5],

        // apply a client side filter to further limit results to those strictly within
        // the Curr Region region
        filter: function (item) {
        // returns true if item contains Curr Region region
        return item.context.map(function (i) {

        return (i.id.split('.').shift() === 'region' && i.text === 'Gujarat');
        }).reduce(function (acc, cur) {
        return acc || cur;
        });
        },
        mapboxgl: mapboxgl
        }));

        var marker = new mapboxgl.Marker()
  .setLngLat([long,lat])
  .addTo(map);
}

function getLocationCoords(){
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/dark-v10',
        zoom: 13
        });

    //LOC COORDS
    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      };

      function success(pos) {
        var crd = pos.coords;
        temp=crd.latitude;

        placeLocator(crd.latitude,crd.longitude);
        //console.log('Your current position is:');
        console.log(`Latitude : ${crd.latitude}`);
        console.log(`Longitude: ${crd.longitude}`);
        //console.log(`More or less ${crd.accuracy} meters.`);
      }

      function error(err) {
        console.warn(`ERROR(${err.code}): ${err.message}`);
      }

      var x=navigator.geolocation.getCurrentPosition(success, error, options);

    }

    getLocationCoords();


