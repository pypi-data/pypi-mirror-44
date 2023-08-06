import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware, {ThunkMiddleware} from 'redux-thunk';
import { createLogger } from 'redux-logger';
import rootReducer from './reducers';
import { convertKeysToCamelCase, appData } from './tools';
import { State, AllProjectData } from './types';

const loggerMiddleware = createLogger();

export default function configureStore() {

    let initialStoreData: State = {} as State;
    if (appData.initialData) {
        Object.assign(initialStoreData, convertKeysToCamelCase<AllProjectData>(appData.initialData));
        initialStoreData.projectDataAge = Object.values(initialStoreData.projects).reduce((map, p) => (map[p.id] = new Date().getTime(), map), {})
        console.debug(initialStoreData);
    }

    return createStore(rootReducer, initialStoreData, applyMiddleware(thunkMiddleware as ThunkMiddleware, loggerMiddleware))

}
