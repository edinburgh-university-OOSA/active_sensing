// A script to view a single Sentinel-1 scene

// Open the Sentinel-1 collection and filter for VH
var imgVH = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VH');

// separate ascending and descending orbits, for consistent geometry
var ascVH = imgVH.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));

// Select a two month window
var dates = ee.Filter.date('2021-09-25', '2021-11-25');

// take the mean backscatter fornthe time window. This is despeckling in time
var scatterVH = ascVH.filter(dates).mean();

// make the map
Map.setCenter( -3.9 ,56.8, 8); // Center on Scotland
Map.addLayer(scatterVH, {min: -25, max: 5}, 'S-1 backscatter', true);

