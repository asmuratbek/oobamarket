import React from "react";
import createClass from "create-react-class";


var CategoryList = createClass({
    displayName: 'CategoryList',

    handleCategoriesSort: function (e) {
        e.preventDefault();
        this.props.categorySort(e.target.getAttribute('data-id'));
    },

    render: function () {
        // var children = [];
        var parent_id = this.props.index;
        var descendants = this.props.descendants;

        return (
            <li className={this.props.category.id == this.props.activeCategory ? "uk-open" : ""}>
                    <a className="uk-accordion-title uk-display-block uk-text-left" href={`#${this.props.category.id}`}
                       onClick={this.handleCategoriesSort}
                       data-id={this.props.category.id}
                       data-parent="#accordion">{this.props.category.title}</a>

                    <div id={this.props.category.id} className="uk-accordion-content">
                        {descendants}
                    </div>
            </li>

        )
    }
});

module.exports = CategoryList;
