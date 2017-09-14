import React from "react";
import { Button } from "react-bootstrap";

import LOGO from "./images/logo.jpeg";
import Styles from "./app.less";

export class App extends React.Component {
    render() {
        return (
            <div className={Styles.logo}>
                NMDD
                <img src={LOGO} />
            </div>
        );
    }
}