// A script to extract a time series of Landsat-8 NDVI data

// point of interest
var geometry = /* color: #d63000 */ee.Geometry.Point([-1.8159373680132496,55.518401138401934]);

// Open the Sentinel-1 collection for VH
var imgVH = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VH');

// clip to tiles over our point and separate ascending orbits
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

// export the timeseries


