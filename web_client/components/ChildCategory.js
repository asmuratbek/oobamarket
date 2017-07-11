import React from 'react';
import createClass from 'create-react-class';
import _ from 'lodash';


var ChildCategory = createClass({
  displayName: 'ChildCategory',

  handleCategoriesSort: function(e){
    e.preventDefault();
    // if (_.indexOf(this.props.activeCategories, this.props.category)!=-1){
    //   e.target.parentElement.className = "";
    // }
    // else {
    //   e.target.parentElement.className += "active ";
    // }
    // this.props.onChangeCategory(e.target.text);
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

              <a href={this.props.parent_id} className="active">{this.props.child.title}</a>

          )
  }
});

module.exports=ChildCategory;
