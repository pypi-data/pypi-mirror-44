import * as React from 'react';

import Dashboard from '../containers/Dashboard';
import Login from './Login';
import { Paper, createMuiTheme, MuiThemeProvider } from '@material-ui/core';
import { colors } from '@material-ui/core';
import { appData } from '../tools';

const lightTheme = createMuiTheme({
    palette: {
        type: 'light',
        primary: colors.blue,
    },
    typography: {
        useNextVariants: true,
    }
});

const darkTheme = createMuiTheme({
    palette: {
        type: 'dark',
        primary: colors.cyan,
        secondary: colors.pink,
    },
    typography: {
        useNextVariants: true,

    }
});

// #006699

type Props = {
    isDarkTheme: boolean,
}

export default React.memo((props: Props) => {
    let { isDarkTheme } = props;
    return (
        <MuiThemeProvider theme={isDarkTheme ? darkTheme : lightTheme}>
            <Paper style={{ height: '100%' }}>
                {appData.isLoggedIn ? <Dashboard /> : <Login />}
            </Paper>
        </MuiThemeProvider>
    )
})
