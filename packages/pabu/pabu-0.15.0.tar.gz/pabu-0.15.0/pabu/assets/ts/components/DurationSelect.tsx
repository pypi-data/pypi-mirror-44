import * as React from 'react';
import { Select, MenuItem } from '@material-ui/core';

export type Props = {
    value: number,
    onChange: (duration: number) => void,
}

const values = ['Show all', '1 day', '3 days', '5 days', '1 week', '2 weeks', '4 weeks', '8 weeks'];

export type State = {
    value: string,
}

const units = {
    d: 24*3600,
    w: 24*7*3600,
}

export default class DurationSelect extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props)
        this.state = {
            value: this.valueToString(props.value),
        }
    }

    private valueToString(val: number): string {
        if (val == 0)
            return values[0];
        for (const v of values.slice(1)) {
            if (this.valueToNumber(v) == val)
                return v;
        }
        return values[0];
    }

    private valueToNumber(val: string): number {
        if (val == values[0])
            return 0;
        const [amount, unit] = val.split(' ');
        return parseInt(amount) * units[unit[0]];
    }

    render() {
        return <Select
                margin="dense"
                inputProps={{name: 'status', id: 'status'}}
                onChange={ev => {
                    this.props.onChange(this.valueToNumber(ev.target.value))
                    this.setState({value: ev.target.value});
                }}
                value={this.state.value}
                SelectDisplayProps={{style: {fontSize: 14, padding: '2px 24px 2px 1px'}}}
            >
            {values.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
            </Select>
    }
}
