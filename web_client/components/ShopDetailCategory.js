import React from 'react';
import createClass from 'create-react-class';
import _ from 'lodash';
import ChildCategory from './ChildCategory';


var CategoryList = createClass({
  displayName: 'CategoryList',

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
    if (category.descendants.length) {
      console.log('yes')
    }
    else {
      console.log("no")
    }

    return (
      <div></div>
    )
  },

  render: function(){
    return (
              <li className="active">
                  <a  role="button" data-toggle="collapse" href={this.props.category.id} aria-expanded="false" aria-controls="collapseExample">{this.props.category.title}</a>

                      {this.getDescendants(this.props.category)}

              </li>
          )
  }
});

module.exports=CategoryList;
