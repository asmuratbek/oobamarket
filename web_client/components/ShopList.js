import React from 'react';
import createClass from 'create-react-class';
import Shop from './Shop';


var ShopList = createClass({
  displayName: 'ShopList',

  render: function(){
    var filteredShops = [];
    var queryText = this.props.q;

    this.props.shops.forEach(function(item) {
      if(item.title.toLowerCase().indexOf(queryText)!=-1)
      {
        filteredShops.push(item)
      }
    });

    filteredShops = filteredShops.map(function(item, index) {
      return(
        <Shop key = { index }
          shop = { item } />
      ) //return
    }.bind(this));

    return(
          <div>
            <div className="search_query">
                <h3>Рекомендуемые продавцы</h3>
                <p>Магазины, в которых найден ваш товар</p>
            </div>

            <div className="recommended_sellers">

                {filteredShops}

            </div>
          </div>
    )
  }
});

module.exports=ShopList;
