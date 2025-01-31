import React, { Component } from 'react';
import { render } from 'react-dom';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import Loader from 'react-loader';

const tiles =  'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
const attr = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
// const tiles = 'http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg'
// const attr = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const mapCenter = [13, 12];
const zoomLevel = 2;
const ChatIcon = L.Icon.extend({ options: { iconSize: [20, 20] }});

class HeatMap extends Component {
  
  getIconColour(polarity) {
    if (polarity === 0) 
      return new ChatIcon({iconUrl: 'chatbubblered.png'});
    else if (polarity === 2) 
      return new ChatIcon({iconUrl: 'chatbubbleblue.png'});
    else 
      return new ChatIcon({iconUrl: 'chatbubblegreen.png'});
  }

  getMarkers(tweets) {

    return (
      tweets.map(x => x.location.length ?
        <div>
          <Marker position={x.location} 
                  icon={this.getIconColour(x.polarity)}
                  key={x.id}>
              <Popup>
                <div>{x.text}</div>
              </Popup>
          </Marker> 
        </div>
      : null)
    )
  }

  getMapTiles() {
    return (
      <div>
        <TileLayer attribution={attr} url={tiles} />
        {this.getMarkers(this.props.tweets)}  
      </div>
    )
  }

  getLoader() {
    const style = {'position': 'absolute',
                   'marginLeft': '30%',
                   'bottom': '25%',
                   'fontSize': '20px',
                   'font': 'Helvetica' }
    return (
      <div>
        <Loader length={20} width={10} radius={30} scale={1.00} />
        <span style={style}>Fetching results, this may take a moment...</span>
      </div>
    )
  }

  render() {
    // console.log(this.props.tweets)
    return (
      <Map center={mapCenter} zoom={zoomLevel} worldCopyJump={true}>
        {this.props.loaded ? this.getMapTiles() : this.getLoader()}
      </Map>
    );
  }
}

export default HeatMap;