
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#page").toggleClass("active");
});

//Maps
function initialize() {
    $('.map-canvas').each(function() {
        var theaterInfo = $(this).html();
        theaterInfo = $.parseJSON(theaterInfo);
        var myLatlng = new google.maps.LatLng(theaterInfo.latitude, theaterInfo.longitude);
        var mapOptions = {
            zoom: 14,
            center: myLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }
        var map = new google.maps.Map((this), mapOptions);

        var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: theaterInfo.title,});

        var contentString = '<div id="map-info">'+
          '<a href="http://maps.google.com/maps?saddr=&daddr=' + theaterInfo.address + '" target ="_blank">Get Directions<\/a>'
          '</div>';

        var infowindow = new google.maps.InfoWindow({
          content: contentString,
          maxWidth: 100,
        });

        google.maps.event.addListener(marker, 'click', function() {
            infowindow.open(map,marker);
        });
  });
}


google.maps.event.addDomListener(window, 'load', initialize);


