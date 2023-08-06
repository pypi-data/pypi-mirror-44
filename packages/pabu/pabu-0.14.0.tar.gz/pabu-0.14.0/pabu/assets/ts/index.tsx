import * as React from "react";
import * as ReactDOM from "react-dom";

import {CssBaseline} from '@material-ui/core';
import * as ReactTooltip from 'react-tooltip'

import '../scss/app.scss';

import { library } from '@fortawesome/fontawesome-svg-core';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import Root, { store } from "./containers/Root";
import { fetchTickingStat, openProject, setDarkTheme } from "./actions";
import { pabuLocalStorage, appData } from "./tools";

library.add(fab, fas, far);

if (appData.isLoggedIn) {
    store.dispatch(fetchTickingStat());
    if (pabuLocalStorage.openedProjectId)
        store.dispatch(openProject(pabuLocalStorage.openedProjectId));

    let isDarkTheme = pabuLocalStorage.isDarkTheme;
    store.dispatch(setDarkTheme(isDarkTheme));
}

ReactDOM.render(
    <React.Fragment>
        <CssBaseline />
        <Root/>
        <ReactTooltip effect="solid" className="pb-tooltip"/>
    </React.Fragment>,
    document.getElementById("body")
);
