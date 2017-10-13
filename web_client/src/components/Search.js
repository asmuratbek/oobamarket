import React, {Component} from "react";
import DayPickerInput from "react-day-picker/DayPickerInput";
import "react-day-picker/lib/style.css";
import data from "../fixtures/23.json";
import {getTickets} from "../actions/tickets";
import {connect} from "react-redux";
import {bindActionCreators} from "redux";


class Search extends Component {
  constructor(props) {
    super(props)
    this.state = {}
   }
  search = () => {
    this.props.getTickets(data.Tickets)
  }
  render() {
    return (
      <div className="search">
        <div className="block_form">
          <input className="block_form__input" placeholder="Откуда"/>
          <div className="reverse"></div>
        </div>
        <div className="block_form">
          <input className="block_form__input" placeholder="Куда"/>
        </div>
        <div className="block_form block_form-small">
          <DayPickerInput className="block_form__input" placeholder="Туда"/>
        </div>
        <div className="block_form block_form-small">
          <DayPickerInput className="block_form__input" placeholder="Обратно"/>
        </div>
        <div className="block_form">
          <select name="" id="" className="block_form__input block_form__input-select">
            <option value="l">Взрослый</option>
            <option value="m">Детский</option>
            <option value="s">Младенец</option>
          </select>
          <input type="number" className="block_form__input block_form__input-number" placeholder="1"/>
        </div>
        <div className="block_form block_form-button" onClick={this.search}>поиск</div>
      </div>
    )
  }
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({getTickets}, dispatch)
}

export default connect(null, mapDispatchToProps)(Search)
