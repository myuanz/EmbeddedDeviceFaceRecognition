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



class GetUsers extends React.Component {
    constructor(props) {
        super(props);
        register_event_callback('get_users', (data) => {
            this.setState({
                users: data
            })
        });
        emit("get_users")
    }
    state = {
        users: [],
        to_add_user: {
            name: '',
            ID: '',
        }
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

                    <h3>已有用户</h3>

                    <table>
                        <tr>
                            <th>ID</th>
                            <th>姓名</th>
                        </tr>                        {
                            this.state.users.map((user) => {
                                return (
                                    <tr>
                                        <td>{user.ID}</td>
                                        <td>{user.name}</td>
                                    </tr>
                                )

                            })
                        }
                    </table>
                </Paper>
                <Paper>
                    <form>
                        <TextField name={'name'} label="姓名"
                            value={this.state.to_add_user.name}
                            onChange={this.handleAccountChange} />
                        <TextField name={'ID'} label="学工号"
                            value={this.state.to_add_user.ID}
                            onChange={this.handleAccountChange} />
                        <Button variant="outlined" color="primary" onClick={
                            () => {
                                console.log(this.state.to_add_user);
                                emit('create_association', this.state.association_uid, this.state.to_add_user.ID);
                            }
                        }>
                            创建用户
                        </Button>
                    </form>
                </Paper>

            </div>

        );
    }

}
export {
    GetUsers
}