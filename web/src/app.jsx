import _ from "lodash";

import React from "react";
import { Button } from "react-bootstrap";
import classnames from "classnames";

import { action, observable } from "mobx";
import { observer } from "mobx-react";

import LOGO from "./images/logo.jpeg";
import GIPHY from "./images/ted_mixing.gif";
import CAM from "./images/cam.gif";
import Styles from "./app.less";

class StateIdle extends React.Component {
    constructor(...props) {
        super(...props);
    }

    componentWillMount() {

    }

    componentWillUnmount() {
    }

    render() {
        return (
            <div className={Styles.logo}>
                Dear NMDD, Make Me a Drink <br/><br/>
                <Button bsStyle="danger" bsSize="large" style={{}} onClick={this._on_start_lucky}>I'm Feeling Lucky!</Button><br />
                <Button bsStyle="danger" bsSize="large" onClick={this._on_start_best}>Give Me Your Best.</Button>
            </div>
        );
    }


    _on_start_lucky = () => {
        this.props.app.push("DRINK", {style: "LUCKY"});
    };

    _on_start_best = () => {
        this.props.app.push("DRINK", {style: "BEST"});
    };
}

class StatePouring extends React.Component {
    constructor(...props) {
        super(...props);
    }

    componentWillMount() {

    }

    componentWillUnmount() {
    }

    render() {
        return (
            <div style={{textAlign:"center"}}><img src={GIPHY} /><br />{this.props.state.status}</div>
        );
    }
}

class FeedbackQuestion extends React.Component {
    render() {
        const { question, result } = this.props;

        return (
            <div>
                <span style={{fontSize:20}}>{question}</span><br/><br/>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 10})} bsStyle="success" bsSize="large" onClick={() => this._select(10)}>Loved it!<br/>10</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 9})} bsStyle="success" bsSize="large" onClick={() => this._select(9)}>9</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 8})} bsStyle="success" bsSize="large" onClick={() => this._select(8)}>8</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 7})} bsStyle="warning" bsSize="large" onClick={() => this._select(7)}>7</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 6})} bsStyle="warning" bsSize="large" onClick={() => this._select(6)}>6</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 5})} bsStyle="warning" bsSize="large" onClick={() => this._select(5)}>5</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 4})} bsStyle="warning" bsSize="large" onClick={() => this._select(4)}>4</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 3})} bsStyle="danger" bsSize="large" onClick={() => this._select(3)}>3</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 2})} bsStyle="danger" bsSize="large" onClick={() => this._select(2)}>2</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 1})} bsStyle="danger" bsSize="large" onClick={() => this._select(1)}>1</Button>
                    <Button className={classnames({[Styles.feedbackSelected]: result === 0})} bsStyle="danger" bsSize="large" onClick={() => this._select(0)}>Terrible!<br/>0</Button><br/><hr/>
            </div>
        );
    }

    _select(result) {
        this.props.onResult(result);
    }
}

@observer
class StateFeedback extends React.Component {
    constructor(...props) {
        super(...props);

        this.data = observable.object({
            questions: [
                {type: "general", question: "Did you like your drink?", result: null},
                {type: "sourness", question: "Did you like the sourness of your drink?", result: null},
                {type: "sweetness", question: "Did you like the sweetness of your drink?", result: null},
                {type: "strength", question: "Did you like the strength of your drink?", result: null},
            ]
        });
    }

    componentWillMount() {

    }

    componentWillUnmount() {
    }

    render() {
        return (
            <div style={{textAlign:"center"}}>
                {
                    this.data.questions.map(({question, result}, idx) => (
                        <FeedbackQuestion key={idx}
                            question={question}
                            result={result}
                            onResult={(result) => this._handle_result(idx, result)} />
                    ))
                }
            </div>
        );
    }

    _handle_result(idx, result) {
        this.data.questions[idx].result = result;

        if (_.every(this.data.questions, ({result}) => null !== result)) {
            this.props.app.push("FEEDBACK", this.data.questions)
        }
    }

}

class StateCamera extends React.Component {
    constructor(...props) {
        super(...props);
        this._video = null;
        this._canvas = null;
        this._captures = [];
    }
    componentWillMount() {

    }

    componentWillUnmount() {
    }

    render() {
        return (
            <div style={{textAlign:"center"}}>
                <img src={CAM} width="100" /><br /><br />
                <video ref={this._on_video} width="500" /><br />
                <canvas ref={this._on_canvas} style={{visibility: "hidden"}} />
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
                    setTimeout(() => this.props.app.push("DONE", this._captures), delay + 1000);
                };
            })
            .catch(function(err) { console.log(err.name + ": " + err.message); });
    }

    _capture() {
        let context = this._canvas.getContext("2d");
        this._canvas.width = this._video.videoWidth;
        this._canvas.height = this._video.videoHeight;
        context.drawImage(this._video, 0, 0, this._canvas.width, this._canvas.height);

        this._captures.push(this._canvas.toDataURL("image/png"));
        console.log("CAPTURE");
    }
}

@observer
export class App extends React.Component {
    static STATES = {
        "idle": StateIdle,
        "pouring": StatePouring,
        "feedback": StateFeedback,
        "capturing": StateCamera
    };
    constructor(...props) {
        super(...props);

        this._ws = null;
        this._ws_url = `wss://${document.location.host}/realtime`;
        
        this.data = observable.shallowObject({
            state: null
        });
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

    push(action, data=null) {
        this._ws.send(JSON.stringify({action: action, data: data}));
    }

    render() {
        if (null === this.data.state) {
            return <b>LOADING</b>;
        }

        const cls = App.STATES[this.data.state.view] || null;
        if (null === cls) {
            return <b>UNKNOWN STATE {this.data.state.view}</b>;
        }

        return React.createElement(cls, {
            app: this,
            state: this.data.state
        });
    }

    _on_ws_open = () => {
        console.info("WEBSOCKET Open");
    };

    _on_ws_error = () => {
        console.error("WEBSOCKET Error");
    };

    _on_ws_message = (message) => {
        console.info("WEBSOCKET Message", message.data);

        this.data.state = JSON.parse(message.data).state;
    };
}