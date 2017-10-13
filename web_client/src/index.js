import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./components/App";
import registerServiceWorker from "./registerServiceWorker";
import {applyMiddleware, createStore} from "redux";
import {Provider} from "react-redux";
import {ConnectedRouter, routerMiddleware} from "react-router-redux";
import reducer from "./reducers";
import createHistory from "history/createBrowserHistory";
import {composeWithDevTools} from "redux-devtools-extension";

const history = createHistory()
const middleware = routerMiddleware(history)
const store = createStore(reducer, composeWithDevTools(applyMiddleware(middleware)))

ReactDOM.render(
  <Provider store={store}>
    <ConnectedRouter history={history}>
      <App />
    </ConnectedRouter>
  </Provider>,
  document.getElementById('root')
);
registerServiceWorker();
