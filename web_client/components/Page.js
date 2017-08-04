import React from 'react';
import createClass from 'create-react-class';

var Page = createClass({
    displayName: 'Page',
    activeClass: function(){
        if (this.props.page == this.props.currentPage) {
            return "active"
        } else {
            return ""
        }
    },
    render: function(){
        return (
            <li><a className={`${this.activeClass()}`} href={this.props.link}>{this.props.page}</a></li>
        )
    }
});

module.exports=Page;
