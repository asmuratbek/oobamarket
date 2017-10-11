import React, {Component} from "react";

class Ticket extends Component {
  constructor(props) {
    super(props)
    this.state = {}
   }
  render() {
    return (
      <div className="ticket">
        <div className="ticket__price">{this.props.Total.KGS.view}</div>
        <div className="ticket__logo"></div>
        <div className="ticket__name">{this.props.Way_1[0].Segments[0].Airline_Human.name_ru}</div>
        <div className="ticket__way">
          <div className="time"></div>
          <div className="time"></div>
        </div>
        <div className="ticket__book">Забронировать</div>
      </div>
    )
  }
}

export default Ticket
