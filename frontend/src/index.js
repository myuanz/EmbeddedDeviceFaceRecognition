import React from 'react';
import ReactDOM from 'react-dom';

import {subscribeToTimer} from './api/subscribeToTimer';

class App extends React.Component {
    constructor(props) {
        super(props);
        subscribeToTimer((err, timestamp) => this.setState({
            timestamp: timestamp
        }));
    }

    state = {timestamp: 'no timestamp yet'}

    render() {
        return (
            <h1>This is the timer value: {this.state.timestamp}</h1>
        );
    }
}

ReactDOM.render(<App/>, document.getElementById('root'));
