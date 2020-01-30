import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Box from '@material-ui/core/Box';
import Paper from '@material-ui/core/Paper';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    useParams
} from "react-router-dom";
import { GetUsers } from "./views/get_users";
import { GetFeature } from "./views/get_feature";
import { ResponsiveDrawer } from "./views/nav";

class App extends React.Component {

    constructor(props) {
        super(props);
    }
    render() {
        return (
            <Router>
                <div>
                    <ul>
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                        <li>
                            <Link to="/about">About</Link>
                        </li>
                        <li>
                            <Link to="/dashboard">Dashboard</Link>
                        </li>
                    </ul>

                    <hr />
                    <Switch>
                        <Route exact path="/">
                            <Home />
                        </Route>
                        <Route path="/about">
                            <About />
                        </Route>
                        <Route path="/dashboard">
                            <Dashboard />
                        </Route>
                    </Switch>
                </div>
                <div>
                <ResponsiveDrawer>
                    <div>123</div>
                </ResponsiveDrawer>
                <GetUsers />
                <GetFeature />
            </div>
            </Router>
            
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'));
