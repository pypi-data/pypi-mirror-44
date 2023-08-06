
import * as React from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogContentText, TextField, DialogActions, Select, InputLabel, MenuItem, FormControl } from '@material-ui/core';

import { PaymentSubmitData, UserMap, User } from '../types';
import moment = require('moment');
import { dialogTransition } from './tools';

type Props = {
    opened: boolean,
    onSubmit: (data: PaymentSubmitData) => void,
    onClose: () => void,
    users: Array<User>,
}


export default class PaymentDialog extends React.Component<Props, PaymentSubmitData> {

    state = {
        user_id: null,
        amount: '',
        note: '',
        time: '',
    }

    onSubmit = (ev: React.SyntheticEvent) => {
        ev.preventDefault();
        if (this.state.user_id != null)
            this.props.onSubmit(this.state);
    }

    render() {
        let {users, onClose, opened} = this.props;

        return <Dialog
            open={opened}
            onClose={onClose}
            aria-labelledby="form-dialog-title"
            TransitionComponent={dialogTransition}
        >
            <DialogTitle id="form-dialog-title">Add time entry</DialogTitle>
            <form onSubmit={this.onSubmit} id="create_project_form">
                <DialogContent>
                    <DialogContentText>Add amount of time you spent on this task. Examples: 3h, 3h 30m, 17m. (h: hours, m: minutes)</DialogContentText>
                    <TextField
                            autoFocus
                            margin="dense"
                            id="amount"
                            label="Amount"
                            type="text"
                            required
                            onChange={ev => {this.setState({amount: ev.target.value})}}
                            fullWidth
                        />
                        <TextField
                            margin="dense"
                            id="time"
                            label="Time"
                            type="datetime-local"
                            defaultValue={moment().format("YYYY-MM-DDTHH:mm")}
                            required
                            onChange={ev => {this.setState({time: ev.target.value})}}
                            fullWidth
                        />
                    <FormControl fullWidth required>
                        <InputLabel htmlFor="user">User</InputLabel>
                        <Select
                            margin="dense"
                            inputProps={{
                                name: 'user',
                                id: 'user',
                            }}
                            onChange={ev => {this.setState({user_id: parseInt(ev.target.value)})}}
                            value={this.state.user_id > 0 ? this.state.user_id : ''}
                        >
                        {users.map(user => <MenuItem key={user.id} value={user.id}>{user.name}</MenuItem>)}
                        </Select>
                    </FormControl>
                    <TextField
                        margin="dense"
                        id="note"
                        label="Note"
                        type="text"
                        multiline
                        fullWidth
                        onChange={ev => {this.setState({note: ev.target.value})}}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={this.props.onClose} color="primary">Cancel</Button>
                    <Button type="submit" color="primary">Submit</Button>
                </DialogActions>
            </form>
        </Dialog>
    }
}
