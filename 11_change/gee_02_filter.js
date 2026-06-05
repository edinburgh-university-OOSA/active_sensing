// A script to threshold and plot a DEM

var image = ee.Image('CGIAR/SRTM90_V4');  // read SRTM

// Threshold the DEM
var thresh=914;                           // threshold
var dem = image.select(['elevation']);    // read the elevation layer
var subset1 = image.updateMask(dem.gte(thresh)); // subset that is greater than or equal to thresh

// Center on Scotland
Map.setCenter( -3.9 ,56.8, 8);

// Display the image on the map.
Map.addLayer(image, {min: 0, max: 1345}, 'SRTM elevation (m)');
Map.addLayer(subset1, {min: 0, max: 1345,palette: ['red']}, 'SRTM over 914 m (m)');

