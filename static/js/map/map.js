var osmLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>',
	thunLink = '<a href="http://thunderforest.com/">Thunderforest</a>';

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
	osmAttrib = '&copy; ' + osmLink + ' Contributors',
	landUrl = 'http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',
	thunAttrib = '&copy; '+osmLink+' Contributors & '+thunLink;

var mapUrl = 'http://otile4.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.png',
	mapAttrib = '&copy; ' + osmLink + ' Contributors';

var osmMap = L.tileLayer(osmUrl, {attribution: osmAttrib}),
	landMap = L.tileLayer(landUrl, {attribution: thunAttrib});

var aerial= L.tileLayer(mapUrl, {attribution: mapAttrib});

var dataurl = '/parcel_data/'
var buildingsurl = '/buildings_data/'
var boundaryurl = '/boundary_data/'


var parcel= L.geoJson();
var building= L.geoJson();
var boundary = L.geoJson();


function eStyle(feature) {
	return {
		weight: 2,
		//opacity: 1,
		color: 'grey',
		dashArray: '3',
		fillOpacity: 0.6,
		//fillColor: 'brown'
	};
}
function bStyle(feature) {
	return {
		weight: 2,
		//opacity: 1,
		color: 'black',
		dashArray: '3',
		fillOpacity: 0.3,
		fillColor: 'black'
	};
}
function doStyleparcel(feature) {
	switch (feature.properties.sale){
		case false:
			return {
				weight: 2.0,
				opacity: 1.0,
				color: 'brown',
				fillColor: 'brown',
				//dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case true:
			return {
				weight: 2,
				opacity: 1,
				color: 'blue',
				fillColor: 'blue',
				//dashArray: '3',
				fillOpacity: 0.7
			};
			break;			
			

	}

}

var map = L.map('map',{
	layers: [osmMap],
	keyboard: true,
	boxZoom: true,
	zoomControl: true,
	//measureControl: true,
	doubleClickZoom: true,
	scrollWheelZoom: true,
	fullscreenControl: true,
	fullscreenControlOptions: {
		position: 'topleft'
	} 
	}).setView([-0.421897, 36.951358], 15);
	mapLink ='<a href="http://openstreetmap.org">OpenStreetMap</a>';
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: 'Map data &copy; ' + mapLink,
			    maxZoom:32,
			    }).addTo(map);
				

// add the new control to the map


var measureControl = L.control.measure({
	position: 'topleft',
	completedColor: '#C8F2BE'
});
measureControl.addTo(map);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);


// control that shows state info on hover
$.getJSON(dataurl, function (data) {
    parcel.addData(data).setStyle(doStyleparcel);
    parcel.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.objectid + "<br>" + "Area: " + e.target.feature.properties.shape_area + "<br>" + " Length : " + e.target.feature.properties.shape_leng +  "<br>" + "Number: " + e.target.feature.properties.number + "<br>" + "On Sale: " + e.target.feature.properties.sale + "<br>" + "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//locations.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});

$.getJSON(buildingsurl, function (data) {
    building.addData(data).setStyle(eStyle);
    building.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.objectid + "<br>" + "Building_n: " + e.target.feature.properties.building_n + "<br>" +  "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//locations.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});
$.getJSON(boundaryurl, function (data) {
    boundary.addData(data).setStyle(bStyle);
    boundary.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//locations.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});
var legend = L.control({position:'bottomleft'});
legend.onAdd = function (map) {
	var div = L.DomUtil.create('div','info legend');
	div.innerHTML = "<h3>Legend</h3><table></table>";
	return div;
}
legend.addTo(map);

map.addLayer(parcel)


var baseLayers = {
	"OSM Mapnik": osmMap,
	"Landscape": landMap,
	"Aerial":aerial
};

var overlays = {
	"Parcels": parcel,
	"Buildings": building,
	"Boundary": boundary,
	
};

L.control.layers(baseLayers,overlays,{collapsed:false}).addTo(map);
L.control.scale({position:"bottomleft"}).addTo(map);
