import React, {Component} from 'react';

class CategoryList extends Component {
    handleCategoriesSort = (e) => {
        e.preventDefault();
        this.props.categorySort(e.target.getAttribute('data-id'));
    }

    render () {
        let parent_id = this.props.index;
        let descendants = this.props.descendants;

        return (
             <li className={this.props.category.id === this.props.activeCategory ? "uk-open" : ""}>
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
}

export default CategoryList;
