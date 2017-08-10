import React from 'react';
import createClass from 'create-react-class';


var SearchForm = createClass({
  displayName: 'SearchForm',

  handleSort: function(e) {
      this.props.onReOrder(e.target.value);
  }, //handleSort

  handlePriceFromChange: function(e) {
    this.props.onChangePriceFrom(e.target.value)
  },

  handlePriceToChange: function(e){
    this.props.onChangePriceTo(e.target.value)
  },

  search: function (e) {
    this.props.onSearch(e.target.value)
  },

  render: function(){
    return (
      <div className="form-filter">
                <form className="form-inline">

                    <div className="form-group select">
                        <select className="form-control" value={this.props.orderBy} onChange={this.handleSort}>
                            <option value="-created_at">Сначала новые </option>
                            <option value="title">По названию</option>
                            <option value="price">Цена по возрастанию</option>
                            <option value="-price">Цена по убыванию </option>
                        </select>
                    </div>

                    <div className="form-group input price">
                        <input type="number" className="form-control" placeholder="от 2000 сом" value={this.props.priceFrom} onChange={this.handlePriceFromChange} />
                    </div>

                    <div className="form-group input price">
                        <input type="number" className="form-control" placeholder="до 4000 сом" value={this.props.priceTo} onChange={this.handlePriceToChange} />
                    </div>

                     <div className="form-group search-input">
                        {/*<select className="form-control" value={this.props.deliveryType} onChange={this.handleDeliveryType}>*/}
                            {/*<option value="all">Доставка (все виды)</option>*/}
                            {/*<option value="free">Бесплатная</option>*/}
                            {/*<option value="paid">Платная</option>*/}
                            {/*<option value="self">Самовывоз</option>*/}
                        {/*</select>*/}
                         <input type="text" className="form-control" placeholder="Поиск товара" onChange={this.search} value={this.props.query} />
                         {/*<button type="submit">*/}
                            {/*<span className="glyphicon glyphicon-search"></span>*/}
                        {/*</button>*/}
                    </div>

                </form>
            </div>

    )
  }
});

module.exports=SearchForm;
