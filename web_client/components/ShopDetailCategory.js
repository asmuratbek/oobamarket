import React from 'react';
import createClass from 'create-react-class';
import _ from 'lodash';
import ChildCategory from './ChildCategory';


var CategoryList = createClass({
    displayName: 'CategoryList',

    handleCategoriesSort: function (e) {
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

    render: function () {
        // var children = [];
        var parent_id = this.props.index;
        var descendants = this.props.descendants;
        //
        children = this.props.category.descendants.map(function(item, index) {
          return (
            <ChildCategory
                            key={index}
                            category={item}
                            onChangeCategory={changeCategory}
                            activeCategory={activeCategory}
                            categorySort={handleChildCategorySort}
                        />
          )
        });

        return (
            <li className={this.props.category.id == this.props.activeCategory ? "uk-open" : ""}>
                    <a className="uk-accordion-title uk-display-block uk-text-left" href={`#${this.props.category.id}`}
                       onClick={this.handleCategoriesSort}
                       data-id={this.props.category.id}
                       data-parent="#accordion">{this.props.category.title}</a>

                    <div id={this.props.category.id} className="uk-accordion-content">

                    </div>
            </li>

        )
    }
});

module.exports = CategoryList;
