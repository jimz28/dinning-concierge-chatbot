import React, { Component } from 'react';
import { PageHeader, ListGroup } from 'react-bootstrap';
import { API } from 'aws-amplify';
import Chatbox from './chatbox';
import './Home.css';

export default class Home extends Component {
	constructor(props) {
		super(props);

		this.state = {
			isLoading: true,
			testApiCall: []
		};
	}

	// async componentDidMount() {
	// 	if (!this.props.isAuthenticated) {
	// 		return;
	// 	}

	// 	try {
	// 		const testApiCall = await this.testApiCall();
	// 		this.setState({ testApiCall });
	// 	} catch (e) {
	// 		alert(e);
	// 	}

	// 	this.setState({ isLoading: false });
	// }

	// testApiCall() {
	// 	return API.get('testApiCall', '/hello');
	// }

	// renderTestAPI(testApiCall) {
	// 	console.log(testApiCall);
	// 	return testApiCall.message;
	// }

	renderLander() {
		return (
			<div className="lander">
				<h1>Welcome to Dining Concierge Service</h1>
				<br/>
				<h3>Please Log In to Start Your Chat with Our Agent</h3>
			</div>
		);
	}

	renderTest() {
		return (
			<div className="test">
				<PageHeader>Our agent is ready to help you</PageHeader>
				<h3>Click the cloud button at the lower right to start your chat</h3>
				<Chatbox />
			</div>
		);
	}

	render() {
		return <div className="Home">{!this.props.isAuthenticated ? this.renderLander() : this.renderTest()}</div>;
	}
}
