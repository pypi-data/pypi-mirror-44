import * as React from 'react'
import { Provider } from 'react-redux'
import configureStore from '../store'
import App from '../containers/App';

export const store = configureStore();

export default class Root extends React.Component {
    render() {
        let data = window['initialData'];
        return (
            <Provider store={store}>
                <App isLoggedIn={data.isLoggedIn} userInfo={data.userInfo} authBackendNames={data.authBackendNames} version={data.version} />
            </Provider>
        )
    }
}
