// Ola Lysien's code from 2021 MSc dissertation
// https://code.earthengine.google.com/1ecec95d2e96223ebf29ee589c63cea9


//Set AOI, t10tel covers both study areas A (G1) and B (G2)
var AOI = angle2

// Adding a NDVI band
function addNDVI(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('ndvi');
  return image.addBands([ndvi]);
}

// Adding a Moisture band for testing of most appropriate index of change
function addNDWI(image) {
  var ndwi = image.normalizedDifference(['B3', 'B5']).rename('ndwi');
  return image.addBands([ndwi]);
}

// Cloud masking of Sentinel-2 L1C
function maskS2clouds(image) {
  var qa = image.select('QA60');
  
  // Bits 10 and 11 are clouds and cirrus, respectively. 
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11; 
  
  // Both flags should be set to zero, indicating clear conditions. 
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  
  return image.updateMask(mask);
}


// Creating the Sentinel-2 Image-Collection 
var collection = ee.ImageCollection('COPERNICUS/S2')
    .filterDate('2018-08-06','2018-08-08')
    .map(maskS2clouds)
    .map(addNDVI)
    .map(addNDWI)
//    .filter(ee.Filter.eq('CLOUDY_PIXEL_PERCENTAGE', 0))
    .filter(ee.Filter.bounds(AOI)); // CHNAGE BACK TO TABLE 
    
// View the median composite
var vizParams = {bands: ['B4', 'B3', 'B2'], min: 0, max: 2000};
Map.addLayer(collection.median(), vizParams, 'collection');

var getImage = function(id) {
  return ee.Image(collection.filter(ee.Filter.eq('system:index', id)).first())
}

//Sentinel-2 image collection to extract points for each pixel 
var collectionX = ee.ImageCollection('COPERNICUS/S2')
    .filterDate('2017-06-01','2021-05-30')
    .map(addNDVI)
    .map(addNDWI)
    .filter(ee.Filter.bounds(AOI));  
    
//Make a point in the center of a 5x5 sentinel pixel window 
var sentinelpixels = ee.Image(collectionX.first()).clip(AOI);
var img = sentinelpixels.addBands(ee.Image.pixelLonLat())

var samples = img.sample({
  region: AOI,
  scale: 50,
  numPixels: 1204899790,
  dropNulls:false,
  geometries: true 
})

//coarsen the pixels by prodcuing bounding boxes around the previously extracted points 
var bounding_box_func = function(feature) {
    var intermediate_buffer = feature.buffer(25);  // buffer radius to produce 5x5 pixel-window 
    var intermediate_box = intermediate_buffer.bounds(); // Draw a bounding box around the central pixel point 
      return(intermediate_box); // Return the bounding box
      };

// Apply function
 var bounding_boxes = samples.map(bounding_box_func);
    Map.centerObject(samples); // Center map on sample points
    Map.addLayer(bounding_boxes, {color: '#FECA1E'}, "Bounding boxes");

// print(bounding_boxes.size());

//Subset the Study Areas into 5000 pixel windows 
 var chunk = 5000
 var collectionSize = 174172
 for (var i = 0; i<collectionSize;i=i+chunk){
   var subset = ee.FeatureCollection(bounding_boxes.toList(chunk,i));
   Export.table.toAsset(subset, "subset", "G4_subset_")
 }

//assign a specific id to each bounding box (coarsened pixel)
var box_id = function(feature) {
  return ee.Feature(feature.geometry(), {'id': feature.id()});
};
 
//select data subsets from above i.e. G1_S1 and repeat for all 
var boxes = bounding_boxes.map(box_id); 

// specify the subset numers to label the csv later on 
var no = '1' 

//Mulissa et al. (2020) Implementaion of Sentinel-1 Backscatter ARD Data Framework 
//Sentinel 1 Processed data 
var wrapper = require('users/adugnagirma/gee_s1_ard:wrapper');
var helper = require('users/adugnagirma/gee_s1_ard:utilities');

//---------------------------------------------------------------------------//
// DEFINE PARAMETERS
//---------------------------------------------------------------------------//

var parameter = {//1. Data Selection
              START_DATE: "2017-07-30",
              STOP_DATE: "2021-02-08",
              POLARIZATION:'VVVH',
              ORBIT : 'BOTH',
              GEOMETRY: AOI, //uncomment if interactively selecting a region of interest
              //GEOMETRY: ee.Geometry.Polygon([[[104.80, 11.61],[104.80, 11.36],[105.16, 11.36],[105.16, 11.61]]], null, false), //Uncomment if providing coordinates
              //GEOMETRY: ee.Geometry.Polygon([[[112.05, -0.25],[112.05, -0.45],[112.25, -0.45],[112.25, -0.25]]], null, false),
              //2. Additional Border noise correction
              APPLY_ADDITIONAL_BORDER_NOISE_CORRECTION: true,
              //3.Speckle filter
              APPLY_SPECKLE_FILTERING: true,
              SPECKLE_FILTER_FRAMEWORK: 'MULTI',
              SPECKLE_FILTER: 'BOXCAR',
              SPECKLE_FILTER_KERNEL_SIZE: 9,
              SPECKLE_FILTER_NR_OF_IMAGES: 10,
              //4. Radiometric terrain normalization
              APPLY_TERRAIN_FLATTENING: true,
              DEM:ee.Image('USGS/SRTMGL1_003'),
              TERRAIN_FLATTENING_MODEL: 'VOLUME',
              TERRAIN_FLATTENING_ADDITIONAL_LAYOVER_SHADOW_BUFFER: 0,
              //5. Output
              FORMAT : 'DB',
              CLIP_TO_ROI: true,
              SAVE_ASSETS: false
}

//---------------------------------------------------------------------------//
// DO THE JOB
//---------------------------------------------------------------------------//
      

//Preprocess the S1 collection
var s1_preprocces = wrapper.s1_preproc(parameter);

var s1 = s1_preprocces[0]
s1_preprocces = s1_preprocces[1]

//---------------------------------------------------------------------------//
// VISUALIZE
//---------------------------------------------------------------------------//

//Visulaization of the first image in the collection in RGB for VV, VH, images
var visparam = {}
if (parameter.POLARIZATION=='VVVH'){
     if (parameter.FORMAT=='DB'){
    var s1_preprocces_view = s1_preprocces.map(helper.add_ratio_lin).map(helper.lin_to_db2);
    var s1_view = s1.map(helper.add_ratio_lin).map(helper.lin_to_db2);
    visparam = {bands:['VV','VH','VVVH_ratio'],min: [-20, -25, 1],max: [0, -5, 15]}
    }
    else {
    var s1_preprocces_view = s1_preprocces.map(helper.add_ratio_lin);
    var s1_view = s1.map(helper.add_ratio_lin);
    visparam = {bands:['VV','VH','VVVH_ratio'], min: [0.01, 0.0032, 1.25],max: [1, 0.31, 31.62]}
    }
}
else {
    if (parameter.FORMAT=='DB') {
    s1_preprocces_view = s1_preprocces.map(helper.lin_to_db);
    s1_view = s1.map(helper.lin_to_db);
    visparam = {bands:[parameter.POLARIZATION],min: -25,max: 0}   
    }
    else {
    s1_preprocces_view = s1_preprocces;
    s1_view = s1;
    visparam = {bands:[parameter.POLARIZATION],min: 0,max: 0.2}
    }
}



Map.centerObject(parameter.GEOMETRY, 12);

Map.addLayer(s1_view, visparam, 'First image in the input S1 collection', true);
Map.addLayer(s1_preprocces_view, visparam, 'First image in the processed S1 collection', true);

var inang = s1_preprocces;
print('angle is', inang);
//---------------------------------------------------------------------------//
// EXPORT
//---------------------------------------------------------------------------//

//Convert format for export
if (parameter.FORMAT=='DB'){
  s1_preprocces = s1_preprocces.map(helper.lin_to_db);
}

//Save processed collection to asset
if(parameter.SAVE_ASSETS) {
helper.Download.ImageCollection.toAsset(s1_preprocces, '', 
               {scale: 10, 
               region: s1_preprocces.geometry(),
                type: 'float'})
}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////


// create time-series of slected pixels to quickly visually assess the data 
var testPoint1 = ee.Feature(boxes.toList(13).get(3))

//Incidence Angle 
var chart = ui.Chart.image.series({
    imageCollection: s1_preprocces.select('angle'),
    region: AOI
    }).setOptions({
      interpolateNulls: true,
      lineWidth: 1,
      pointSize: 3,
      //title: 'Incidence Angle (Degrees)',
      vAxis: {title: 'Incidence Angle (Degrees)'},
      hAxis: {title: 'Date', format: 'YYYY-MMM', gridlines: {count: 12}}

    })
print(chart)   



//VVVH Ratio 
var chart = ui.Chart.image.series({
    imageCollection: s1_preprocces_view.select('VVVH_ratio'),
    region: testPoint1.geometry()
    }).setOptions({
      interpolateNulls: true,
      lineWidth: 1,
      pointSize: 3,
      title: 'Backscatter over Time at a Single Location',
      vAxis: {title: 'VV/VH'},
      hAxis: {title: 'Date', format: 'YYYY-MMM', gridlines: {count: 12}}

    })
print(chart) 

//Time-series extarction for all pixel windows for VVVH ratio 
var s1_preprocces_vvvh = s1_preprocces_view.select('VVVH_ratio')
var triplets = s1_preprocces_vvvh.map(function(image) {
  return image.select('VVVH_ratio').reduceRegions({
    collection: boxes, 
    reducer: ee.Reducer.mean().setOutputs(['VVVH_ratio']), 
    scale: 10,
  })// reduceRegion doesn't return any output if the image doesn't intersect
    // If there was no vvvh ratio value found, we set the vvvh ratio to a NoData value -9999
    .map(function(feature) {
    var VVVH_ratio = ee.List([feature.get('VVVH_ratio'), -9999])
      .reduce(ee.Reducer.firstNonNull())
    return feature.set({'VVVH_ratio': VVVH_ratio, 'date': ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')})
    })
  }).flatten();

var format = function(table, rowId, colId) {
  var rows = table.distinct(rowId); 
  var joined = ee.Join.saveAll('matches').apply({
    primary: rows, 
    secondary: table, 
    condition: ee.Filter.equals({
      leftField: rowId, 
      rightField: rowId
    })
  });
        
  return joined.map(function(row) {
      var values = ee.List(row.get('matches'))
        .map(function(feature) {
          feature = ee.Feature(feature);
          return [feature.get(colId), feature.get('VVVH_ratio')];
        });
      return row.select([rowId]).set(ee.Dictionary(values.flatten()));
    });
};

var sentinelResults = format(triplets, 'id', 'date');

Export.table.toDrive({
    collection: sentinelResults,
    description: 'VVVH_ratio' + no,
    folder: 'earthengine',
    fileNamePrefix: 'VVVH_ratio_' + no,
    fileFormat: 'CSV'
})

