import React from 'react';
import ReactDOM from 'react-dom';

import {
    subscribeToTimer,
    register_recv_callback,
    send_message_to_device,
    register_event_callback,
    emit
} from './api/subscribeToTimer';

class App extends React.Component {
    constructor(props) {
        let device_info = [];
        super(props);
        subscribeToTimer((err, timestamp) => this.setState({
            timestamp: timestamp
        }));
        register_recv_callback((data) => {
            console.log(data);
            device_info.push(data);
            this.setState({
                device_info_out: JSON.stringify(data, null, 2) + '\n' + this.state.device_info_out
            })
        });
        register_event_callback('get_users', (data) => {
            this.setState({
                users: data
            })
        });

        emit('get_users');
    }

    state = {
        timestamp: 'no timestamp yet',
        device_info_out: "",
        users: [],
        to_add_user: {
            name: '',
            ID: '',
        },
        association_uid: ''
    };
    handleAccountChange = (event) => {
        let old_data = this.state.to_add_user;
        old_data[event.target.name] = event.target.value;

        this.setState({
            to_add_user: old_data
        });
    };
    handleAssociationChange = (event) => {
        this.setState({
            association_uid: event.target.value
        });

    };

    render() {
        return (
            <div>
                <textarea
                    value={this.state.device_info_out}
                    style={{width: '100%', height: 500}}
                />
                <button onClick={
                    () => {
                        send_message_to_device('get_cfg', {})
                    }
                }>获取配置
                </button>

                <button onClick={
                    () => {
                        send_message_to_device('set_cfg', {
                            'cfg': {
                                'uart_baud': 115200,
                                'out_feature': 0,
                                'open_delay': 1,
                                'pkt_fix': 0,
                                'auto_out_feature': 1,
                                'out_interval_in_ms': 500,
                                'fea_gate': 70,
                            }
                        })
                    }
                }>切换至添加模式
                </button>
                <button onClick={
                    () => {
                        send_message_to_device('set_cfg', {
                            'cfg': {
                                'uart_baud': 115200,
                                'out_feature': 0,
                                'open_delay': 1,
                                'pkt_fix': 0,
                                'auto_out_feature': 2,
                                'out_interval_in_ms': 500,
                                'fea_gate': 70,
                            }
                        })
                    }
                }>切换至识别模式
                </button>
                <button onClick={
                    () => {
                        send_message_to_device('query_face', {
                            'query': {
                                "total": 1,
                                "start": 0,
                                "end": 10,
                                "out_feature": 0
                            }
                        })
                    }
                }>获取人脸数
                </button>
                <hr/>
                                <h3>已有用户</h3>

                <table>
                    <tr>
                        <th>ID</th>
                        <th>姓名</th>
                    </tr>
                    {
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

                <hr/>
                <label>
                    姓名:
                    <input
                        name={'name'}
                        value={this.state.to_add_user.name}
                        onChange={this.handleAccountChange}/>
                </label>
                <label>
                    学号:
                    <input
                        name={'ID'}
                        value={this.state.to_add_user.ID}
                        onChange={this.handleAccountChange}/>
                </label>

                <button onClick={
                    () => {
                        console.log(this.state.to_add_user);
                        emit('create_user', ...Object.values(this.state.to_add_user));
                        emit('get_users')
                    }
                }>创建账号
                </button>
                <hr/>
                <label>
                    UID:
                    <input
                        name={'UID'}
                        value={this.state.association_uid}
                        onChange={this.handleAssociationChange}/>
                </label>
                <label>
                    学号:
                    <input
                        name={'ID'}
                        value={this.state.to_add_user.ID}
                        onChange={this.handleAccountChange}/>
                </label>
                <button onClick={
                    () => {
                        console.log(this.state.to_add_user);
                        emit('create_association', this.state.association_uid, this.state.to_add_user.ID);

                    }
                }>创建关联
                </button>
            </div>

        );
    }
}

ReactDOM.render(<App/>, document.getElementById('root'));
