
import * as React from 'react';
import { Button, Dialog, DialogTitle, DialogContent, TextField, DialogActions } from '@material-ui/core';
import { NameDescSubmitCallback } from '../types';
import { dialogTransition } from './tools';

type State = {
    name: string,
    desc: string,
}

type Props = {
    opened: boolean,
    onSubmit: NameDescSubmitCallback,
    caption: string,
    initialData: State,
    onClose: () => void,
}

export default class ProjectFormDialog extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props);
        this.state = props.initialData;
    }

    componentWillReceiveProps(props: Props) {
        this.setState(props.initialData)
    }

    onSubmit = (ev: React.SyntheticEvent) => {
        ev.preventDefault();
        this.props.onSubmit(this.state.name, this.state.desc);
    }

    render() {
        let {name, desc} = this.state;
        return <Dialog
            open={this.props.opened}
            onClose={this.props.onClose}
            aria-labelledby="form-dialog-title"
            TransitionComponent={dialogTransition}
        >
            <DialogTitle id="form-dialog-title">{this.props.caption}</DialogTitle>
            <form onSubmit={this.onSubmit} id="create_project_form">
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Name"
                        type="text"
                        required
                        value={name || ''}
                        onChange={ev => {this.setState({name: ev.target.value})}}
                        fullWidth
                    />
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
