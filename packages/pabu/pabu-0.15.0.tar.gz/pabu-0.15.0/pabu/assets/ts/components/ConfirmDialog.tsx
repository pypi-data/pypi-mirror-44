import * as React from 'react';
import { ConfirmDialogContex } from '../types';
import { Dialog, DialogContent, DialogActions, Button, Typography } from '@material-ui/core';
import { dialogTransition } from './tools';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export type StateProps = {
    confirmDialogContex: ConfirmDialogContex
}

export type DispatchProps = {
    closeDialog: (action: () => any) => void,
}

export default React.memo((props: StateProps & DispatchProps) => {
    return <Dialog
        open={props.confirmDialogContex.show}
        onClose={() => props.closeDialog(null)}
        TransitionComponent={dialogTransition}
    >
        <DialogContent style={{display: 'flex', alignItems: 'center'}}>
            <Typography><FontAwesomeIcon icon="question-circle" style={{fontSize: '3em', marginRight: 20}} /></Typography>
            <Typography variant="h6">{props.confirmDialogContex.message}</Typography>
        </DialogContent>
        <DialogActions>
            <Button onClick={() => props.closeDialog(null)} color="primary">Cancel</Button>
            <Button onClick={() => props.closeDialog(props.confirmDialogContex.callback)} color="primary">OK</Button>
        </DialogActions>
    </Dialog>
})
