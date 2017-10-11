import React from "react";
import createClass from "create-react-class";


var Shop = createClass({
  displayName: 'Shop',

  render: function(){
    return(
            <div className="img-wrapper">
                <a href={this.props.shop.get_absolute_url}></a>
                <img src={this.props.shop.logo} alt={this.props.shop.title}/>
            </div>
    )
  }
});

module.exports=Shop;
