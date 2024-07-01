// Initialize and add the map
const heartImg = document.createElement("img");

// heartImg.src =
let map;
async function initMap() {
  // The location of Uluru
  const position = { lat: -33.865143, lng: 151.209900 };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  map = new Map(document.getElementById("map"), {
    zoom: 10,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  // The marker, positioned at Uluru
  const marker= new AdvancedMarkerElement({
    map: map,
    position: position,
    // content: heartImg,
    title: "Sydney",
  });
}

initMap();