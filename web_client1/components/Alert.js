import React, {Component} from "react";
import AlertContainer from "react-alert";

export default class App extends Component {
  alertOptions = {
    offset: 14,
    position: 'bottom left',
    theme: 'light',
    time: 5000,
    transition: 'scale',
  }

  showAlert = () => {
    this.msg.show('Some text or component', {
      time: 3000,
      type: 'success',
      icon: <img src="http://merp.mx/lib/css/icon/success-32.png" />
    })
  }

  render () {
    return (
      <div>
        <AlertContainer ref={a => this.msg = a} {...this.alertOptions} />
        <button onClick={this.showAlert}>Show Alert</button>
      </div>
    )
  }
}
