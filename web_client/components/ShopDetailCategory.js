import React from 'react';
import createClass from 'create-react-class';
import _ from 'lodash';
import ChildCategory from './ChildCategory';


var CategoryList = createClass({
  displayName: 'CategoryList',

  handleCategoriesSort: function(e){
    e.preventDefault();
    console.log(e.target.getAttribute('data-id'));
    this.props.categorySort(e.target.getAttribute('data-id'));

    // if (_.indexOf(this.props.activeCategories, this.props.category)!=-1){
    //   e.target.parentElement.className = "";
    // }
    // else {
    //   e.target.parentElement.className += "active ";
    // }
    // this.props.onChangeCategory(e.target.text);
  },

  // getDescendants: function(category){
  //   if (category.descendants.length) {
  //     console.log('yes')
  //   }
  //   else {
  //     console.log("no")
  //   }
  //
  //   return (
  //       <div></div>
  //   )
  // },

  render: function(){
    // var children = [];
    var parent_id = this.props.index;
    //
    // children = this.props.category.descendants.map(function(item, index) {
    //   return (
    //     <ChildCategory
    //       key={index}
    //       child={item}
    //       index={index}
    //       parent_id={parent_id}
    //     />
    //   )
    // });

    return (
              <li className={this.props.category.id == this.props.activeCategory ? "active":""}>
                  <a  role="button" data-toggle="collapse" href='#' aria-expanded="false" aria-controls="collapseExample" onClick={this.handleCategoriesSort} data-id={this.props.category.id}>{this.props.category.title}</a>
                    {this.props.category.descendants.length ?
                        <div className="collapse category-in-category" id={this.props.index}>
                        </div>
                    : ""}

              </li>
          )
  }
});

module.exports=CategoryList;
