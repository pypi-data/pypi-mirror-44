import * as React from 'react';
import PabuTable, {TableColDesriptor} from './PabuTable';
import { ExpandedPayment } from '../types';
import moment = require('moment');
import { formatDuration } from '../tools';
import { Button } from '@material-ui/core';

export type OwnProps = {
    id: number,
}

export type StateProps = {
    rows: Array<ExpandedPayment>,
}

export type DispatchProps = {
    onDelete: (entry: ExpandedPayment) => void,
    onAddPayment: (projectId: number) => void,
}

export default React.memo((props: StateProps & DispatchProps & OwnProps) => {
    const {rows, onDelete, id, onAddPayment} = props;

    const rowDescriptors = [
        new TableColDesriptor('time', 'Time', v => moment.unix(v).format('YYYY-MM-DD HH:mm')),
        new TableColDesriptor('amount' , 'Amount', formatDuration),
        new TableColDesriptor('createdUserName', 'Created'),
        new TableColDesriptor('paidUserName', 'Paid'),
        new TableColDesriptor('note', 'Note'),
    ]

    const controllCellHeader = <div>
        <Button size="small" color="primary" onClick={onAddPayment.bind(this, id)}>Add</Button>
    </div>

    return <PabuTable colDescriptors={rowDescriptors} rows={rows} onDelete={onDelete} controllCellHeader={controllCellHeader} />
})
