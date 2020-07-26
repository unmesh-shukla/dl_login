import React, {Component} from 'react';
import './css/main.css';
import './css/util.css';
import './signup.css';
import Sketch from "react-p5";


const axios = require('axios');
let video;

export class Signup extends Component {

    constructor(props) {
        super(props);
        this.state = {
            signup : true
        };
        this.stop = this.stop.bind(this);
        this.validateFields = this.validateFields.bind(this);
    }

    setup(p5, canvasParentRef) {

        // Setup Video from p5 captured webcam
        p5.noCanvas();
        video = p5.createCapture(p5.VIDEO);
        var vid =  document.querySelector("video");
        var tb = document.querySelector(".wrap-input100");
        tb.after(vid);


        // Setup event listeners
        const button = document.getElementById('submit');
        button.addEventListener('click', async event => {
            if (this.validateFields() === true) {

                    const mood = document.getElementById('mood').value;
                    video.loadPixels();

                    const image64 = video.canvas.toDataURL();

                    const response = await axios.post(
                                        'http://localhost:80/register',
                                        {'image64': image64, 'username': mood}
                                    );

                    this.stop();

                    if (response.data.status === 200) {
                        alert("You are successfully registered! Login with your face.");
                        this.props.backhome();
                    }
                    else if (response.data.message){
                        alert(response.data.message);
                        this.props.backhome();
                    }
                    else {
                        // alert("An unknown error occurred.");
                        this.props.backhome();
                    }
                }
            }
        );
    }

    stop() {
        const tracks = document.querySelector("video").srcObject.getTracks();
          tracks.forEach(function(track) {
            track.stop();
        });
    }

    validateFields() {

        let username = document.getElementById('mood').value;

        if (username !== undefined) {
            let spaces_arr = username.split(" ");
            let spaces = spaces_arr.length - 1;

            if (spaces !== 0 || username.length === 0) {
                this.setState({
                    invalid_username: true
                });
            }
            else {
                this.setState({
                    invalid_username: false
                });
            }
        }

        if (this.state.invalid_username === undefined) {
            return false
        }
        else {
            return !this.state.invalid_username;
        }
    }


    logout() {
        const tracks = document.querySelector("video").srcObject.getTracks();
            tracks.forEach(function(track) {
                track.stop();
            });
        this.props.backhome();
    }

    render() {

        let signup = (
                <div>
                    <div className="limiter">
                        <div className="container-login100">
                            <div className="wrap-login100 p-l-110 p-r-110 p-t-62 p-b-33">
                                <span className="login100-form-title">
                                    Sign Up
                                </span>
                                {this.state.signup?<Sketch id="s" setup={this.setup.bind(this)} draw={this.draw}/>:''}
                                <div className="wrap-input100">
                                    <input id="mood" className="input100" type="text" name="username" placeholder="Enter username"></input>

                                    <div className="validate-input">
                                        {
                                            this.state.invalid_username?
                                            <span>Please enter a valid username</span>
                                            :
                                            ""
                                        }
                                    </div>
                                </div>

                                <div className="container-login100-form-btn m-t-17">
                                    <button id="submit" className="login100-form-btn">
                                        Sign Up
                                    </button>
                                </div>
                                <div className="container-login100-form-btn m-t-17">
                                    <button onClick={this.logout.bind(this)} className="login100-form-btn">
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
            { signup }
            </div>
        )
    }
}
export default Signup;
