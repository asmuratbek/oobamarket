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
    var children = [];
    var parent_id = this.props.index;

    children = this.props.category.descendants.map(function(item, index) {
      return (
        <ChildCategory
          key={index}
          child={item}
          index={index}
          parent_id={parent_id}
        />
      )
    });

    return (
              <li className={this.props.index == 0 ? "active":""}>
                  <a  role="button" data-toggle="collapse" href={`#${this.props.index}`} aria-expanded="false" aria-controls="collapseExample">{this.props.category.title}</a>
                    {this.props.category.descendants.length ?
                        <div className="collapse category-in-category" id={this.props.index}>
                              {children}
                        </div>
                    : ""}

              </li>
          )
  }
});

module.exports=CategoryList;
