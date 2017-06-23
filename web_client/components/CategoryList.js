import React from 'react';
import createClass from 'create-react-class';


var CategoryList = createClass({
  displayName: 'CategoryList',

  render: function(){
    return (

            <li className="active"><a href="">{this.props.category}</a></li>

    )
  }
});

module.exports=CategoryList;
