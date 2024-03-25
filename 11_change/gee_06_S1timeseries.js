// A script to extract a time series of Landsat-8 NDVI data

// point of interest
// var geometry: Point (-1.82, 55.52)

// Open the Sentinel-1 collection for VH
var imgVH = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VH');

// Need to clip the data before doing the filter step. Do it in space, with the GEE instructions.

// separate ascending orbits
var ascVH = imgVH.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));


// Create a chart.
var chart = ui.Chart.image.series({
  imageCollection: ascVH.select('NDVI'),
  region: geometry,
  reducer: ee.Reducer.first(),
  scale: 30
}).setOptions({title: 'NDVI over time'});

// Display the chart in the console.
print(chart);

