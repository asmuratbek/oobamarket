import React from 'react';
import createClass from 'create-react-class';
import _ from 'lodash';


var ChildCategory = createClass({
  displayName: 'ChildCategory',

  handleCategoriesSort: function (e) {
        e.preventDefault();
        console.log(e.target.getAttribute('data-id'));
        this.props.categorySort(e.target.getAttribute('data-id'));
    },

  getDescendants: function(category){

    // return (
    //   {this.props.category.descendants.toArray ?
    //   <div className="collapse category-in-category" id={this.props.category.descendants.id}>
    //
    //           <a href="1" className="active">{this.props.category.descendants.title}</a>
    //
    //   </div>
    //   : ""}
    // )
  },

  render: function(){
    return (
              <div>
                <a href="#" className={this.props.category.id == this.props.activeCategory ? "active children" : "children"} data-id={this.props.category.id} onClick={this.handleCategoriesSort}>{this.props.category.title}</a>
              </div>
          )
  }
});

module.exports=ChildCategory;
