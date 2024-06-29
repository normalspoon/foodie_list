
function initMap() {
    console.log("hello")
    const center = { lat: 50.064192, lng: -130.605469 };
// Create a bounding box with sides ~10km away from the center point
const defaultBounds = {
  north: center.lat + 0.1,
  south: center.lat - 0.1,
  east: center.lng + 0.1,
  west: center.lng - 0.1,
};
const input = document.getElementById("pac-input");
const options = {
  bounds: defaultBounds,
  componentRestrictions: { country: "aus" },
  fields: ["address_components", "geometry", "icon", "name", "place_id"],
  strictBounds: false,
};
const autocomplete = new google.maps.places.Autocomplete(input, options);
autocomplete.setTypes(['restaurant', 'cafe']);
autocomplete.addListener('place_changed', function(place) {
    console.log(place)
const result = autocomplete.getPlace()
console.log(result)
const placeId = result.place_id
console.log("this is" + placeId);
}) 

}
