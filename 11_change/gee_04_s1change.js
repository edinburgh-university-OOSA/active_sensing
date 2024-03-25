// A script to view a single Sentinel-1 scene

// Open the Sentinel-1 collection for VH
var imgVH = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select('VH');

// separate ascending orbits
var ascVH = imgVH.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));

// dates for two months before and after storm Arwen, skipping the say of the storm
var beforeDates = ee.Filter.date('2021-09-25', '2021-11-25');
var afterDates = ee.Filter.date('2021-11-27', '2022-01-27');

// take the mean backscatter before and after the event
var beforeVH = ascVH.filter(beforeDates).mean();
var afterVH = ascVH.filter(afterDates).mean();

// make the map
Map.setCenter( -1.834475 ,55.524498, 13);
Map.addLayer(beforeVH, {min: -25, max: 5}, 'Before', true);
Map.addLayer(afterVH, {min: -25, max: 5}, 'After', true);

