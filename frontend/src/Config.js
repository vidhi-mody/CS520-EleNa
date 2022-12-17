export const OPENSTREETMAP_API = 'https://nominatim.openstreetmap.org/search?'
export const OVERPASS_API = 'http://overpass-api.de/api/interpreter'
export const ROUTING_API = 'http://localhost:8080/route'
export function FETCH_COORDINATES_FROM_OPENSTREETMAP_API(lat, lon) {
  return `http://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}&zoom=18&addressdetails=1`
}
export function OVERPASS_REQUEST_BODY(circmuference, latitudeSource, longitudeSource, latitudeDestination, longitudeDestination) {
  return `[out:json];way[highway](around:${circmuference},${longitudeSource},${latitudeSource},${longitudeDestination},${latitudeDestination}); (._;>;);out meta;`
}
export function ROUTING_REQUEST_BODY(latitudeSource, longitudeSource, latitudeDestination, longitudeDestination, place, elevationType, elevationPercent) {
  return {
    start: [latitudeSource, longitudeSource],
    end: [latitudeDestination, longitudeDestination],
    place: place,
    type: elevationType,
    percent: elevationPercent
  };
}