import * as React from 'react';

import Dashboard from '../containers/Dashboard';
import Login from './Login';
import { UserInfo } from '../types';
import { Paper, createMuiTheme, MuiThemeProvider } from '@material-ui/core';
import { colors } from '@material-ui/core';

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
    isLoggedIn: boolean,
    userInfo: UserInfo,
    authBackendNames: Array<string>,
    isDarkTheme: boolean,
    version: string,
}


export default class App extends React.Component<Props> {
    render() {
        let { isLoggedIn, userInfo, authBackendNames, isDarkTheme, version } = this.props;
        return (
            <MuiThemeProvider theme={isDarkTheme ? darkTheme : lightTheme}>
                <Paper style={{ height: '100%' }}>
                    {isLoggedIn ? <Dashboard userInfo={userInfo} version={version} /> : <Login authBackendNames={authBackendNames} />}
                </Paper>
            </MuiThemeProvider>
        )
    }
}
