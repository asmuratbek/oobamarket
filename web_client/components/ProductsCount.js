import React from 'react';
import createClass from 'create-react-class';


var ProductsCount = createClass({
  displayName: 'ProductsCount',

  render: function(){
    return (
      <div className="search_query">
                <h3>Результаты поиска</h3>
                <p>По вашему запросу найдено {this.props.count} товаров в следующих категориях</p>
      </div>
    )
  }
});

module.exports=ProductsCount;
