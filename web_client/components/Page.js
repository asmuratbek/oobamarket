import React from 'react';
import createClass from 'create-react-class';

var Page = createClass({
    displayName: 'Page',

    changePage: function(e) {
        e.preventDefault();
        this.props.changePage(this.props.page);
    },

    render: function(){
        return (
            <li><a className={`${this.props.page == this.props.currentPage ? "active" : ""}`} href="" onClick={this.changePage}>{this.props.page}</a></li>
        )
    }
});

module.exports=Page;
