import React from 'react';
import createClass from 'create-react-class';


var CategoryList = createClass({
  displayName: 'CategoryList',

  handleCategoriesSort: function(e){
    e.preventDefault();
    this.props.onChangeCategory(e.target.text);
    if (this.props.activeCategories.indexOf(this.props.category)!=-1){
      e.target.parentElement.className += "active "
    }
    else {
      e.target.parentElement.className = "active "
    }
  },

  render: function(){
    return (
            <li className={this.handleActiveClass}><a href="" onClick={this.handleCategoriesSort}>{this.props.category}</a></li>
          )
  }
});

module.exports=CategoryList;
