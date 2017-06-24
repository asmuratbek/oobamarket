import React from 'react';
import createClass from 'create-react-class';
import _ from 'lodash';


var CategoryList = createClass({
  displayName: 'CategoryList',

  handleCategoriesSort: function(e){
    e.preventDefault();
    if (_.indexOf(this.props.activeCategories, this.props.category)!=-1){
      e.target.parentElement.className = "";
    }
    else {
      e.target.parentElement.className += "active ";
    }
    this.props.onChangeCategory(e.target.text);
  },

  render: function(){
    return (
            <li><a href="" onClick={this.handleCategoriesSort}>{this.props.category}</a></li>
          )
  }
});

module.exports=CategoryList;
