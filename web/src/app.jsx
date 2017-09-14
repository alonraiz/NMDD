import React from "react";
import { Button } from "react-bootstrap";

import LOGO from "./images/logo.jpeg";
import Styles from "./app.less";

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

    render() {
        return (
            <div className={Styles.logo}>
                NMDD
                <img src={LOGO} />
                {}
            </div>
        );
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