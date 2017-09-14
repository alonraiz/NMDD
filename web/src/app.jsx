import React from "react";
import { Button } from "react-bootstrap";

import LOGO from "./images/logo.jpeg";
import GIPHY from "./images/ted_mixing.gif";
import CAM from "./images/cam.gif";
import Styles from "./app.less";

class StateCamera extends React.Component {
    constructor(...props) {
        super(...props);
        this._video = null;
        this._canvas = null;
    }
    componentWillMount() {

    }

    componentWillUnmount() {
    }

    render() {
        return (
            <div style={{textAlign:"center"}}>
                <img src={CAM} width="100" /><br /><br />
                <video ref={this._on_video} width="500" />
                <canvas ref={this._on_canvas} />
            </div>
        );
    }

    _on_canvas = (ref) => {
        this._canvas = ref;
        if (ref === null) {
            return;
        }
    }

    _on_video = (ref) => {
        this._video = ref;
        if (ref === null) {
            return;
        }

        var constraints={audio:false, video:{width:1280, height:720} };
        navigator.mediaDevices.getUserMedia(constraints)
            .then((mediaStream) => {
                this._video.srcObject = mediaStream;
                this._video.onloadedmetadata = () => {
                    this._video.play()
                };
                this._video.onplaying = () => {
                    let delay = 1000;
                    for (let i = 0; i < 5; i++) {
                        setTimeout(() => this._capture(), delay);
                        delay += 1000;
                    }
                };
            })
            .catch(function(err) { console.log(err.name + ": " + err.message); });
    }

    _capture() {
        console.log("CAPTURE");
    }
}

export class App extends React.Component {
    constructor(...props) {
        super(...props);

        this._ws = null;
        this._ws_url = `ws://${document.location.host}/realtime`;
    }
    componentWillMount() {
        this._ws = new WebSocket(this._ws_url);
        this._ws.onopen = this._on_ws_open;
        this._ws.onerror = this._on_ws_error;
        this._ws.onmessage = this._on_ws_message;
    }

    componentWillUnmount() {
        this._ws.close();
    }

    triggerDrink() {
        alert("MIAO!");
    }

    render() {
        const state = "capturing";
        if (state==="idle") {
            return (
                <div className={Styles.logo}>
                    Dear NMDD, Make Me a Drink <br/><br/>
                    <Button bsStyle="danger" bsSize="large" onClick={this.triggerDrink}>Liron!</Button>
                </div>
            );
        }
        else if (state === "pouring") {
            return <div style={{textAlign:"center"}}><img src={GIPHY} /></div>;
        }
        else if (state === "feedback") {
            return <div style={{textAlign:"center"}}>
            <span style={{fontSize:20}}>Did you like your drink?</span><br/><br/>
            <Button bsStyle="success" bsSize="large">Loved it!<br/>10</Button>
            <Button bsStyle="success" bsSize="large">9</Button>
            <Button bsStyle="success" bsSize="large">8</Button>
            <Button bsStyle="warning" bsSize="large">7</Button>
            <Button bsStyle="warning" bsSize="large">6</Button>
            <Button bsStyle="warning" bsSize="large">5</Button>
            <Button bsStyle="warning" bsSize="large">4</Button>
            <Button bsStyle="danger" bsSize="large">3</Button>
            <Button bsStyle="danger" bsSize="large">2</Button>
            <Button bsStyle="danger" bsSize="large">Terrible!<br/>1</Button><br/><hr/>

            <span style={{fontSize:20}}>Did you like the sourness of your drink?</span><br/><br/>
            <Button bsStyle="success" bsSize="large">Loved it!<br/>10</Button>
            <Button bsStyle="success" bsSize="large">9</Button>
            <Button bsStyle="success" bsSize="large">8</Button>
            <Button bsStyle="warning" bsSize="large">7</Button>
            <Button bsStyle="warning" bsSize="large">6</Button>
            <Button bsStyle="warning" bsSize="large">5</Button>
            <Button bsStyle="warning" bsSize="large">4</Button>
            <Button bsStyle="danger" bsSize="large">3</Button>
            <Button bsStyle="danger" bsSize="large">2</Button>
            <Button bsStyle="danger" bsSize="large">Terrible!<br/>1</Button><br/><hr/>

            <span style={{fontSize:20}}>Did you like the sweetness of your drink?</span><br/><br/>
            <Button bsStyle="success" bsSize="large">Loved it!<br/>10</Button>
            <Button bsStyle="success" bsSize="large">9</Button>
            <Button bsStyle="success" bsSize="large">8</Button>
            <Button bsStyle="warning" bsSize="large">7</Button>
            <Button bsStyle="warning" bsSize="large">6</Button>
            <Button bsStyle="warning" bsSize="large">5</Button>
            <Button bsStyle="warning" bsSize="large">4</Button>
            <Button bsStyle="danger" bsSize="large">3</Button>
            <Button bsStyle="danger" bsSize="large">2</Button>
            <Button bsStyle="danger" bsSize="large">Terrible!<br/>1</Button><br/><hr/>

            <span style={{fontSize:20}}>Did you like the bitterness of your drink?</span><br/><br/>
            <Button bsStyle="success" bsSize="large">Loved it!<br/>10</Button>
            <Button bsStyle="success" bsSize="large">9</Button>
            <Button bsStyle="success" bsSize="large">8</Button>
            <Button bsStyle="warning" bsSize="large">7</Button>
            <Button bsStyle="warning" bsSize="large">6</Button>
            <Button bsStyle="warning" bsSize="large">5</Button>
            <Button bsStyle="warning" bsSize="large">4</Button>
            <Button bsStyle="danger" bsSize="large">3</Button>
            <Button bsStyle="danger" bsSize="large">2</Button>
            <Button bsStyle="danger" bsSize="large">Terrible!<br/>1</Button><br/><hr/>

            <span style={{fontSize:20}}>Did you like the strength of your drink?</span><br/><br/>
            <Button bsStyle="success" bsSize="large">Loved it!<br/>10</Button>
            <Button bsStyle="success" bsSize="large">9</Button>
            <Button bsStyle="success" bsSize="large">8</Button>
            <Button bsStyle="warning" bsSize="large">7</Button>
            <Button bsStyle="warning" bsSize="large">6</Button>
            <Button bsStyle="warning" bsSize="large">5</Button>
            <Button bsStyle="warning" bsSize="large">4</Button>
            <Button bsStyle="danger" bsSize="large">3</Button>
            <Button bsStyle="danger" bsSize="large">2</Button>
            <Button bsStyle="danger" bsSize="large">Terrible!<br/>1</Button><br/><hr/>


            </div>;
        }

        else if (state === "capturing") {
            return <StateCamera />;
        }
    }

    _on_ws_open = () => {
        console.info("WEBSOCKET Open");
    };

    _on_ws_error = () => {
        console.error("WEBSOCKET Error");
    };

    _on_ws_message = (message) => {
        console.info("WEBSOCKET Message", message);
    };
}