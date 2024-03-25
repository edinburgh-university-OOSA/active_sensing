// A script to threshold and plot a DTM

// Instantiate an image with the Image constructor.
var image = ee.Image('CGIAR/SRTM90_V4');  // read SRTM

var thresh=914;                           // threshold
var dem = image.select(['elevation']);    // read the elevation layer
var subset1 = image.updateMask(dem.gte(thresh)); // subset that is greater than or equal to thresh
var subset2 = image.updateMask(dem.lt(thresh));  // subset that is less than thresh

// Zoom to a location.
Map.setCenter( -3.9 ,56.8, 8); // Center on Scotland

// Display the image on the map.
Map.addLayer(subset2, {min: 0, max: 1345}, 'custom visualization');                   // less than thresh in greyscale
Map.addLayer(subset1, {min: 0, max: 1345,palette: ['red']}, 'custom visualization');  // greater than thresh in red

