import * as React from 'react'
import { Provider } from 'react-redux'
import configureStore from '../store'
import App from '../containers/App';
import { SnackbarProvider } from 'notistack';

export const store = configureStore();

export default class Root extends React.Component {
    render() {
        return (
            <Provider store={store}>
                <SnackbarProvider maxSnack={3}>
                    <App />
                </SnackbarProvider>
            </Provider>
        )
    }
}
