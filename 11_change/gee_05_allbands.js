// A script to view Sentinel-1 data in every possible combination at two time-steps

// Open the Sentinel-1 collection for VH and VV
var imgVH = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VH');

var imgVV = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VV');

// separate ascending and descending orbits
var descVH = imgVH.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));
var ascVH = imgVH.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));
var descVV = imgVV.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));
var ascVV = imgVV.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));

// dates for two months before and after storm Arwen, skipping the say of the storm
var beforeDates = ee.Filter.date('2021-09-25', '2021-11-25');
var afterDates = ee.Filter.date('2021-11-27', '2022-01-27');

// take the mean backscatter
var beforeVHasc = ascVH.filter(beforeDates).mean();
var afterVHasc = ascVH.filter(afterDates).mean();
var beforeVHdesc = descVH.filter(beforeDates).mean();
var afterVHdesc = descVH.filter(afterDates).mean();
var beforeVVasc = ascVV.filter(beforeDates).mean();
var afterVVasc = ascVV.filter(afterDates).mean();
var beforeVVdesc = descVV.filter(beforeDates).mean();
var afterVVdesc = descVV.filter(afterDates).mean();

// make the map
Map.setCenter( -1.834475 ,55.524498, 13);
Map.addLayer(beforeVHasc, {min: -25, max: 5}, 'VH ascending before', true);
Map.addLayer(afterVHasc, {min: -25, max: 5}, 'VH ascending after', true);
Map.addLayer(beforeVHdesc, {min: -25, max: 5}, 'VH descending before', true);
Map.addLayer(afterVHdesc, {min: -25, max: 5}, 'VH descending after', true);
Map.addLayer(beforeVVasc, {min: -25, max: 5}, 'VV ascending before', true);
Map.addLayer(afterVVasc, {min: -25, max: 5}, 'VV ascending after', true);
Map.addLayer(beforeVVdesc, {min: -25, max: 5}, 'VV descending before', true);
Map.addLayer(afterVVdesc, {min: -25, max: 5}, 'VV descending after', true);


