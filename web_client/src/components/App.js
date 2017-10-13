import React, {Component} from "react";
import Search from "./Search";
import TicketsList from "./TicketsList";
import "../App.css";

class App extends Component {
  render() {
    return (
      <div className="container">
        <Search/>
        <TicketsList/>
      </div>
    )
  }
}

export default App
