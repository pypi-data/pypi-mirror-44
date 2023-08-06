
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { createStyles, IconButton, Table, TableBody, TableCell, TableFooter, TableHead, TablePagination, TableRow, TableSortLabel, Theme, withStyles } from '@material-ui/core';
import * as React from 'react';
import { PabuModel } from '../types';


const styles = ({ palette, typography }: Theme) => createStyles({
    icon: {
        width: 35,
        height: 35,
    },
    controlCell: {
        textAlign: 'center',
    }
});


function defaultRowSort(orderBy: string, a: any, b: any) {
    if (b[orderBy] < a[orderBy])
        return 1;
    if (b[orderBy] > a[orderBy])
        return -1;
    return 0;
}


export type TableCellFormatter<T extends PabuModel = PabuModel> = (v: any, row: T) => React.ReactNode;
export type TableRowSortingFunction<T extends PabuModel = PabuModel> = (a: T, b: T) => number;

export class TableColDesriptor<T extends PabuModel = PabuModel> {
    name: string
    label:  string
    formatter: TableCellFormatter<T>
    sortingFunction: TableRowSortingFunction<T>
    style: React.CSSProperties

    constructor(name: string, label: string, formatter: TableCellFormatter<T> = v => v,
                sortingFunction: TableRowSortingFunction<T> = defaultRowSort.bind(null, name), style: React.CSSProperties = {}) {
        this.name = name;
        this.label = label;
        this.formatter = formatter;
        this.sortingFunction = sortingFunction;
        this.style = style;
    }

    setStyle(style: React.CSSProperties) {
        this.style = style;
        return this;
    }
}

type Props = {
    rows: Array<PabuModel>,
    classes: any,
    colDescriptors: Array<TableColDesriptor>,
    onDelete?: (row: PabuModel, context?: any) => void,
    controllCellHeader?: React.ReactNode,
    controllCellFactory?: (row: PabuModel) => React.ReactNode,
    defaultOrderBy?: string,
    defaultOrder?: "asc" | "desc",
    context?: any,
}

type State = {
    page: number,
    rowsPerPage: number,
    orderBy: string,
    order: "asc" | "desc",
}

function rowSort(sorter: TableRowSortingFunction, isAsc: boolean, a: PabuModel, b: PabuModel) {
    const res = sorter(a, b);
    return isAsc ? res : -res;
}

class PabuTable extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props)
        this.state = {
            page: 0,
            rowsPerPage: 5,
            order: props.defaultOrder || 'desc',
            orderBy: props.defaultOrderBy || props.colDescriptors[0].name,
        }
    }

    private getColDescriptor(name: string): TableColDesriptor {
        for (let desc of this.props.colDescriptors) {
            if (desc.name == name)
                return desc;
        }
        return null;
    }

    private getRows(): Array<PabuModel> {
        const { rows } = this.props;
        const { page, rowsPerPage, order, orderBy } = this.state;
        const desc = this.getColDescriptor(orderBy);
        if (desc && desc.sortingFunction)
            rows.sort(rowSort.bind(null, desc.sortingFunction, order == 'asc'))
        return rows.slice(page * rowsPerPage, (page + 1) * rowsPerPage);
    }

    private handleHeaderClick = (fieldName: string) => {
        if (this.state.orderBy == fieldName)
            this.setState({order: this.state.order == 'asc' ? 'desc' : 'asc'})
        else
            this.setState({orderBy: fieldName})
    }

    render() {
        const { rows, classes, onDelete, colDescriptors: rowDescriptors, controllCellHeader, controllCellFactory, context } = this.props;

        return <Table>
            <TableHead>
                <TableRow>
                    {rowDescriptors.map(field => <TableCell key={field.name}>
                        <TableSortLabel
                            active={field.name == this.state.orderBy}
                            direction={this.state.order}
                            onClick={this.handleHeaderClick.bind(this, field.name)}
                        >
                            {field.label}
                        </TableSortLabel>
                    </TableCell>)}
                    <TableCell className={classes.controlCell}>{controllCellHeader}</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>{
                this.getRows().map(row => <TableRow key={row.id}>
                    {rowDescriptors.map(field => <TableCell style={field.style} key={field.name}>{field.formatter(row[field.name], row)}</TableCell>)}
                    <TableCell className={classes.controlCell} >
                        {controllCellFactory ? controllCellFactory(row) :
                            (onDelete ? <IconButton className={classes.icon} onClick={onDelete.bind(this, row, context)}>
                                <FontAwesomeIcon icon="trash" style={{ fontSize: 12 }} />
                            </IconButton> : null)
                        }
                    </TableCell>
                </TableRow>)
            }</TableBody>
            <TableFooter>
                <TableRow>
                    <TablePagination
                        count={rows.length}
                        page={this.state.page}
                        rowsPerPage={this.state.rowsPerPage}
                        rowsPerPageOptions={[5, 10, 25, 50]}
                        onChangePage={(ev, page) => this.setState({ page })}
                        onChangeRowsPerPage={ev => this.setState({ rowsPerPage: parseInt(ev.target.value) })}
                    />
                </TableRow>
            </TableFooter>
        </Table>
    }
}

export default withStyles(createStyles(styles))(PabuTable);
