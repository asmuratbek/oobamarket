import React from 'react';
import createClass from 'create-react-class';
import Page from './Page';
import _ from 'lodash';

var Pagination = createClass({
    displayName: 'Pagination',

    handlePrevious: function(e){
        e.preventDefault();
        this.props.goToPrevious();
    },

    handleNext: function(e){
        e.preventDefault();
        this.props.goToNext();
    },

    handleChangePage: function(page) {
        this.props.goTo(page);
    },

    render: function(){
        var pages = _.range(1, this.props.pagesCount + 1).map(function(value){
            return(
                <Page
                    key={value}
                    page={value}
                    currentPage={this.props.page}
                    changePage={this.handleChangePage}
                />
            )
        }.bind(this));
        return (
            <nav className="pagination">
                        <ul>
                            {this.props.previous ?
                            <li>
                                <a href="" aria-label="Previous" onClick={this.handlePrevious}>
                                    <span aria-hidden="true">&laquo;</span>
                                </a>
                            </li>
                                : ''}
                            {pages}
                            {this.props.next ?
                            <li>
                                <a href="" aria-label="Next" onClick={this.handleNext}>
                                    <span aria-hidden="true">&raquo;</span>
                                </a>
                            </li>
                                : '' }
                        </ul>
                    </nav>
        )
    }
});

module.exports = Pagination;
