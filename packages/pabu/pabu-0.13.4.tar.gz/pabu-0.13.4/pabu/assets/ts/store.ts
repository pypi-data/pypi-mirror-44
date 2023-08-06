import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware, {ThunkMiddleware} from 'redux-thunk';
import { createLogger } from 'redux-logger';
import rootReducer from './reducers';
import { convertKeysToCamelCase } from './tools';
import { State } from './types';

const loggerMiddleware = createLogger();

export default function configureStore() {

    let initialData: State = {} as State;
    if (window['initialData'].initialData) {
        initialData = convertKeysToCamelCase(window['initialData'].initialData);
        initialData.projectDataAge = Object.values(initialData.projects).reduce((map, p) => (map[p.id] = new Date().getTime(), map), {})
        console.debug(initialData);
    }

    return createStore(rootReducer, initialData, applyMiddleware(thunkMiddleware as ThunkMiddleware, loggerMiddleware))

}
