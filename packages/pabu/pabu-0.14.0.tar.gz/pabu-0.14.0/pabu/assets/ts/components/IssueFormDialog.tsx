
import * as React from 'react';
import { Button, Dialog, DialogTitle, DialogContent, TextField, DialogActions, FormControl, InputLabel, Select, MenuItem, Grow } from '@material-ui/core';
import { IssueStatus } from '../types';
import { dialogTransition } from './tools';

type State = {
    name: string,
    desc: string,
    status: IssueStatus,
}

type Props = {
    opened: boolean,
    onSubmit: (name: string, desc: string, status: IssueStatus) => void,
    initialData: State,
    onClose: () => void,
}

export default class IssueFormDialog extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props);
        this.state = props.initialData;
    }

    componentWillReceiveProps(props: Props) {
        this.setState(props.initialData)
    }

    onSubmit = (ev: React.SyntheticEvent) => {
        ev.preventDefault();
        this.props.onSubmit(this.state.name, this.state.desc, this.state.status);
    }

    render() {
        let {name, desc} = this.state;
        return <Dialog
            open={this.props.opened}
            onClose={this.props.onClose}
            aria-labelledby="form-dialog-title"
            TransitionComponent={dialogTransition}
        >
            <DialogTitle id="form-dialog-title">Create task</DialogTitle>
            <form onSubmit={this.onSubmit} id="create_project_form">
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Summary"
                        type="text"
                        required
                        value={name || ''}
                        onChange={ev => {this.setState({name: ev.target.value})}}
                        fullWidth
                    />
                    <FormControl fullWidth required>
                        <InputLabel htmlFor="status">Status</InputLabel>
                        <Select
                            margin="dense"
                            inputProps={{name: 'status', id: 'status'}}
                            onChange={ev => {this.setState({status: ev.target.value as IssueStatus})}}
                            value={this.state.status}
                        >
                        {Object.values(IssueStatus).map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                        </Select>
                    </FormControl>
                    <TextField
                        margin="dense"
                        id="description"
                        label="Description"
                        type="text"
                        value={desc || ''}
                        multiline
                        onChange={ev => {this.setState({desc: ev.target.value})}}
                        fullWidth
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={this.props.onClose} color="primary">
                        Cancel
                    </Button>
                    <Button type="submit" color="primary">Submit</Button>
                </DialogActions>
            </form>
        </Dialog>
    }
}
