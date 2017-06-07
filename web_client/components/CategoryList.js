import React from 'react';
import createClass from 'create-react-class';


var CategoryList = createClass({
  displayName: 'CategoryList',

  render: function(){
    return (
      <ul className="category-tab">
                <li className="active"><a href="">Коляски</a></li>
                <li><a href="">Автокресла</a></li>
                <li><a href="">Кровати</a></li>
                <li><a href="">Автокресла</a></li>
                <li><a href="">Кровати</a></li>
      </ul>
    )
  }
});

module.exports=CategoryList;
