import {SEARCH_TICKETS} from "../constans";
export const getTickets = tickets => {
  return {
    type: SEARCH_TICKETS,
    tickets
  }
}
