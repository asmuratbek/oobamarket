import React, {Component} from 'react';

class ChildCategory extends Component {
    handleCategoriesSort = (e) =>{
        e.preventDefault();
        this.props.categorySort(e.target.getAttribute('data-id'));
    };

    render () {
        return (
            <a href="#" className={this.props.category.id === this.props.activeCategory ?
                    "uk-display-block uk-open" : "uk-display-block"}
                   data-id={this.props.category.id} onClick={this.handleCategoriesSort}>
                    {this.props.category.title}</a>
        )
    }
}

export default ChildCategory;
