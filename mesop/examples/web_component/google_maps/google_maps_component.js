// google_maps_component.js
import {
    LitElement,
    html,
    css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

// **IMPORTANT:** Replace 'YOUR_API_KEY' with your actual Google Maps API Key
const GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY';
const GOOGLE_MAPS_API_URL = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&callback=initMap&loading=async`;

let mapPromise; // To store the Google Maps API Promise

export class GoogleMapsComponent extends LitElement {
    static properties = {
        center: { type: Array }, // Expecting [latitude, longitude]
        zoom: { type: Number },
        markers: { type: Array }, // Array of marker objects
        clickEvent: { type: String }, // Event handler ID for clicks
        height: { type: String }, // Height of the map
        width: { type: String }, // Width of the map
    };

    static styles = css`
        #map {
            height: 600px; /* Adjust map height as needed */
            width: 100%;
        }
    `;

    constructor() {
        super();
        this.center = [0.0, 0.0];
        this.zoom = 13;
        this.markers = [];
        this.clickEvent = '';
        this._map = null; // Internal Google Map instance
        this._googleMarkers = []; // Array to hold Google Maps Marker objects
    }

    firstUpdated() {
        this._loadGoogleMapsAPI();
    }

    updated(changedProperties) {
        if (changedProperties.has('markers')) {
            this._updateMarkers();
        }
    }

    _loadGoogleMapsAPI() {
        if (mapPromise) return; // API already loading/loaded

        mapPromise = new Promise((resolve) => {
            window.initMap = () => resolve(window.google.maps); // Callback for API load

            const script = document.createElement('script');
            script.src = GOOGLE_MAPS_API_URL;
            script.defer = true;
            script.async = true;
            document.head.appendChild(script);
        });

        mapPromise.then((googleMaps) => {
            this._initializeMap(googleMaps);
        });
    }


    _initializeMap(googleMaps) {
        if (this._map) return; // Prevent re-initialization

        const mapDiv = this.shadowRoot.querySelector('#map');
        if (!mapDiv) return; // Map div not yet rendered

        this._map = new googleMaps.Map(mapDiv, {
            center: { lat: this.center[0], lng: this.center[1] },
            zoom: this.zoom,
            clickableIcons: false,
        });

        this._map.addListener('click', (event) => {
            if (this.clickEvent) {
                this.dispatchEvent(new MesopEvent(this.clickEvent, {
                    latlng: [event.latLng.lat(), event.latLng.lng()] // Send latlng back to Python
                }));
            }
        });
        this._updateMarkers(googleMaps); // Initial marker rendering
    }

    _updateMarkers(googleMaps) {
        if (!this._map) return;

        // Clear existing markers
        this._googleMarkers.forEach(marker => marker.setMap(null));
        this._googleMarkers = []; // Clear the array

        this.markers.forEach(markerData => {
            const googleMarker = new googleMaps.Marker({
                position: { lat: markerData.latlng[0], lng: markerData.latlng[1] },
                map: this._map,
            });
            if (markerData.popup_content) {
                const infoWindow = new googleMaps.InfoWindow({
                    content: markerData.popup_content,
                });
                googleMarker.addListener('click', () => {
                    infoWindow.open(this._map, googleMarker);
                });
            }
            this._googleMarkers.push(googleMarker); // Store marker for clearing later
        });
    }


    render() {
        return html`
            <div id="map"></div>
        `;
    }
}

customElements.define('google-maps-component', GoogleMapsComponent);