import React, {Component} from 'react';

class CategoryList extends Component {
    handleCategoriesSort = (e) => {
        if (this.props.activeCategories.indexOf(this.props.category) !== -1) {
            e.target.parentElement.className = "";
        } else {
            e.target.parentElement.className += "active ";
        }

        this.props.onChangeCategory(e.target.text);
    };

    render () {
        return (
             <li><a href="" onClick={this.handleCategoriesSort}>{this.props.category}</a></li>
        )
    }
}

export default CategoryList;
