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
import {
    register_recv_callback,
    register_event_callback,
    emit
} from '../api/subscribeToTimer';



class GetFeature extends React.Component {
    constructor(props) {
        super(props);
        register_event_callback('get_features', (data) => {
            this.setState({
                features: data
            })
        });

    }
    state = {
        features: [],
    };
    handleAccountChange = (event) => {
        const {
            name,
            value
        } = event.target;

        console.log([name, value]);
        let old_data = this.state.to_add_user;
        old_data[name] = value;
        console.log(old_data[name]);

        this.setState({
            to_add_user: old_data
        });
    };

    render() {
        return (
            <div>

                <Paper style={{ padding: 2 + '%' }}>
                    <h3>已有特征</h3>

                    <table>
                        <tr>
                            <th>#</th>
                            <th>录入时间</th>
                            <th>关联人</th>
                            <th>图片</th>
                            <th>操作</th>
                        </tr>

                        {
                            this.state.features.map((feature, index) => {
                                return (
                                    <tr>
                                        <td>{index}</td>
                                        <td>{feature.name}</td>
                                    </tr>
                                )
                            })
                        }
                    </table>
                </Paper>
                

            </div>

        );
    }

}
export {
    GetFeature
}