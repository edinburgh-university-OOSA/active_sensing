// A script to get used to GEE


// Instantiate an image with the Image constructor.
var image = ee.Image('CGIAR/SRTM90_V4');

// Zoom to a location.
Map.setCenter( -3.9 ,56.8, 8); // Center on Scotland

// Display the image on the map.
Map.addLayer(image, {min: 0, max: 1345}, 'custom visualization');






var imgVH = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VH')
        .map(function(image) {
          var edge = image.lt(-30.0);
          var maskedImage = image.mask().and(edge.not());
          return image.updateMask(maskedImage);
        });

var desc = imgVH.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));
var asc = imgVH.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));

var before = ee.Filter.date('2021-09-25', '2021-11-25');
var after = ee.Filter.date('2021-11-25', '2022-01-25');


Map.setCenter( -2.552560 ,56.893688, 12);
Map.addLayer(before, {min: -25, max: 5}, 'Before', true);
Map.addLayer(after, {min: -25, max: 5}, 'After', true);


