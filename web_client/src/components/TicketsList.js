import React, {Component} from "react";
import {connect} from "react-redux";
import Ticket from "./Ticket";


class TicketsList extends Component {
  constructor(props) {
    super(props)
   }
  render() {
    return (
      <div className="results">
        {this.props.tickets ? this.props.tickets.map((ticket, idx) => <Ticket key={idx} {...ticket}/>) : null}
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {tickets: state.tickets}
}

export default connect(mapStateToProps, null)(TicketsList)
