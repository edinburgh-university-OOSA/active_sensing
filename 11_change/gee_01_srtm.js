// A script to get used to GEE


// Instantiate an image with the Image constructor.
var image = ee.Image('CGIAR/SRTM90_V4');

// Zoom to a location.
Map.setCenter( -3.9 ,56.8, 8); // Center on Scotland

// Display the image on the map.
Map.addLayer(image, {min: 0, max: 1345}, 'custom visualization');

