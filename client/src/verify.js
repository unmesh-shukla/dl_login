import React, {Component} from 'react';
import './css/main.css';
import './css/util.css';
import './verify.css';
import Sketch from "react-p5";


const axios = require('axios');
let video;

export class Verify extends Component {

    constructor(props) {
        super(props);
        this.state = {
            verify : false,
            identity: ''
        };
        this.stop = this.stop.bind(this);
    }

    setup(p5='', canvasParentRef='') {

        // Setup Video from p5 captured webcam
        p5.noCanvas();
        video = p5.createCapture(p5.VIDEO);
        var vid =  document.querySelector("video");
        var tb = document.querySelector(".login100-form-title");
        tb.after(vid);

        // Setup event listeners
        const button = document.getElementById('submit');
        button.addEventListener('click', async event => {

            video.loadPixels();
            const image64 = video.canvas.toDataURL();

            const response = await axios.post(
                                'http://localhost:80/verify',
                                {'image64':image64}
                            );

            this.stop();
            if (response.data.identity) {
                this.setState({
                    verify: true,
                    identity: response.data.identity
                })
            }
            else {
                alert("User face not matched.")
                this.props.backhome();
            }
        });
    }

    stop() {
        const tracks = document.querySelector("video").srcObject.getTracks();
        tracks.forEach(function(track) {
            track.stop();
        });
    }

    logout() {
        this.stop();
        this.props.backhome();
    }

    render() {

        let verify = (
                    <div>
                        <div className="limiter">
                            <div className="container-login100">
                                <div className="wrap-login100 p-l-110 p-r-110 p-t-62 p-b-33">

                                    <span className="login100-form-title">
                                        Sign In
                                    </span>

                                    <Sketch setup={this.setup.bind(this)} draw={this.draw}/>

                                    <div className="container-login100-form-btn m-t-17">
                                        <button id="submit" className="login100-form-btn">
                                            Sign In
                                        </button>
                                    </div>
                                    <div className="container-login100-form-btn m-t-17">
                                        <button onClick={this.logout.bind(this)} className="login100-form-btn" type="submit">
                                            Back
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )


        return (
            <div >
                {
                    this.state.verify? 
                    <div>
                        <h1>Namaste {this.state.identity}!</h1>
                        <button onClick={this.props.backhome} className="container-login100-form-btn">Logout</button>
                    </div>
                    :
                    verify 
                }
            </div>
        )
    }
}

export default Verify;
