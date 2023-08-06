
import * as React from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogContentText, TextField, DialogActions } from '@material-ui/core';
import { dialogTransition } from './tools';

type Props = {
    opened: boolean,
    onSubmit: (token: string) => void,
    onClose: () => void,
}

export default class InviteDialog extends React.Component<Props, {token: string}> {

    onSubmit = (ev: React.SyntheticEvent) => {
        ev.preventDefault();
        this.props.onSubmit(this.state.token);
    }

    render() {
        return <Dialog
            open={this.props.opened}
            onClose={this.props.onClose}
            aria-labelledby="form-dialog-title"
            TransitionComponent={dialogTransition}
        >
            <DialogTitle id="form-dialog-title">Project invitation</DialogTitle>
            <form onSubmit={this.onSubmit}>
                <DialogContent>
                    <DialogContentText>Tokens allows you to join to other projects.</DialogContentText>
                        <TextField
                            autoFocus
                            margin="dense"
                            id="token"
                            label="Token"
                            type="text"
                            required
                            onChange={ev => {this.setState({token: ev.target.value})}}
                            fullWidth
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
