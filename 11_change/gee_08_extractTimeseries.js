// A script to extract a time series of Landsat-8 NDVI data

// point of interest
var geometry = ee.Geometry.Point(-1.8159373680132496,55.518401138401934);

// Open the Sentinel-1 collection for VH
var imgVH = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VH');

// clip to tiles over our point and separate ascending orbits
var ascVH = imgVH.filterBounds(geometry).filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));

print(ascVH)

var filteredCollection = imgVH.select('VH').filter(ee.Filter.bounds(geometry))
print(filteredCollection)

// define a point
var region = ee.Geometry.Point(-1.8159373680132496,55.518401138401934)

var timeseries = ascVH.Feature(region)

// Get a dictionary of means in the region.
var means = ascVH.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: region,
  crs: projection.crs,
  crsTransform: projection.transform,
});





/// OLD BELOW HERE ###########
// extract timseries
var timeseries = ascVH.select('VH').filterBounds(geometry)

// export the timeseries
Export.table.toDrive({
  collection: timeseries,
  description: 's1VH_timeseries',
  fileFormat: 'CSV'
});



var timeSeries = ee.FeatureCollection(filteredCollection.map(function(image) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: testPoint.geometry(),
    scale: 10,
    maxPixels: 1e10
  })
  // reduceRegion doesn't return any output if the image doesn't intersect
  // with the point or if the image is masked out due to cloud
  // If there was no ndvi value found, we set the ndvi to a NoData value -9999
  var ndvi = ee.List([stats.get('ndvi'), -9999])
    .reduce(ee.Reducer.firstNonNull())
 
  // Create a feature with null geometry and NDVI value and date as properties
  var f = ee.Feature(null, {'ndvi': ndvi,
    'date': ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')})
  return f
}))
 
// Check the results
print(timeSeries.first())
 
// Export to CSV
Export.table.toDrive({
    collection: timeSeries,
    description: 'Single_Location_NDVI_time_series',
    folder: 'earthengine',
    fileNamePrefix: 'ndvi_time_series_single',
    fileFormat: 'CSV'
})



