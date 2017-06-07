import React from 'react';
import createClass from 'create-react-class';


var ShopList = createClass({
  displayName: 'ShopList',

  render: function(){
    return(
          <div>
            <div className="search_query">
                <h3>Рекомендуемые продавцы</h3>
                <p>Магазины, в которых найден ваш товар</p>
            </div>

            <div className="recommended_sellers">

                <div className="img-wrapper">
                    <a href="{{ shop.get_absolute_url }}"></a>
                    <img src="{{ shop.get_logo }}" alt="{{ shop.title }}"/>
                </div>

            </div>
          </div>
    )
  }
});

module.exports=ShopList;
