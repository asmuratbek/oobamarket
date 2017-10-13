import {combineReducers} from "redux";
import {routerReducer} from "react-router-redux";
import {SEARCH_TICKETS} from "../constans";


const tickets = (state=[], action) => {
  switch (action.type) {
    case SEARCH_TICKETS:
      return [...action.tickets]
    default: return state
  }
}

export default combineReducers({
  tickets,
  router: routerReducer
})
