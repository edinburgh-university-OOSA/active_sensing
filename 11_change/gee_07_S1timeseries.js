// A script to extract a time series of Landsat-8 NDVI data

// point of interest
var geometry = /* color: #d63000 */ee.Geometry.Point([-1.818780857185811, 55.51643550959151]);

// Open the Sentinel-1 collection for VH
var imgVH = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VH');

// Need to clip the data before doing the filter step. Do it in space, with the GEE instructions.

// separate ascending orbits
var ascVH = imgVH.filterBounds(geometry).filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));


// Create a chart.
var chart = ui.Chart.image.series({
  imageCollection: ascVH.select('VH'),
  region: geometry,
  reducer: ee.Reducer.first(),
  scale: 30
}).setOptions({title: 'VH backscatter over time'});

// Display the chart in the console.
print(chart);

