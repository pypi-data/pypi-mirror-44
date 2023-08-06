import { Button } from '@material-ui/core';
import * as React from 'react';
import { ProjectInvitationToken } from '../types';
import PabuTable, { TableColDesriptor } from './PabuTable';

export type OwnProps = {
    id: number,
}

export type StateProps = {
    rows: Array<ProjectInvitationToken>,
}

export type DispatchProps = {
    onDelete: (entry: ProjectInvitationToken) => void,
    onCreateProjectToken: (projectId: number) => void,
}

export default React.memo((props: StateProps & DispatchProps & OwnProps) => {
    const {rows, onDelete, id, onCreateProjectToken} = props;

    const rowDescriptors = [
        new TableColDesriptor('token' , 'Token'),
    ]

    const controllCellHeader = <div>
        <Button size="small" color="primary" onClick={onCreateProjectToken.bind(this, id)}>Generate</Button>
    </div>

    return <PabuTable colDescriptors={rowDescriptors} rows={rows} onDelete={onDelete} controllCellHeader={controllCellHeader} />
})
