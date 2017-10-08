import React from 'react';
import createClass from 'create-react-class';
import _ from 'lodash';


var ChildCategory = createClass({
  displayName: 'ChildCategory',

  handleCategoriesSort: function (e) {
        e.preventDefault();
        this.props.categorySort(e.target.getAttribute('data-id'));
    },

  render: function(){
    return (

                <a href="#" className={this.props.category.id == this.props.activeCategory ?
                    "uk-display-block uk-open" : "uk-display-block"}
                   data-id={this.props.category.id} onClick={this.handleCategoriesSort}>
                    {this.props.category.title}</a>
          )
  }
});

module.exports=ChildCategory;
