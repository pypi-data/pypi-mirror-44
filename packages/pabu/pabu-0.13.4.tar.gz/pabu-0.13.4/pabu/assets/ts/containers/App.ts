import { connect } from 'react-redux';
import App from '../components/App';
import { State } from '../types';

function mapStateToProps(state: State) {
    const { isDarkTheme } = state;
    return {
        isDarkTheme,
    }
}

export default connect(mapStateToProps)(App);
