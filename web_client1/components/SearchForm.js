import React from "react";
import createClass from "create-react-class";


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
      var query = e.target.value;
      this.props.onSearch(query)
  },

  render: function(){
    return (


            <form data-uk-grid className="uk-grid-small search-global-category">
            <div className="uk-width-1-3@l uk-width-1-2@s uk-padding-remove">
                <div className="bg-white">
                    <select className="uk-select" placeholder="Укажите..." defaultValue="-created_at"
                    onChange={this.handleSort}>
                        <option value="-created_at">Сначала новые</option>
                        <option value="title">По названию</option>
                        <option value="price">Цена по возрастанию</option>
                        <option value="-price">Цена по убыванию</option>
                    </select>
                </div>

            </div>
            <div className="uk-width-1-6@l uk-width-1-2@s">
                <input className="uk-input"  type="number"  placeholder="от 2000 сом"
                       value={this.props.priceFrom} onChange={this.handlePriceFromChange} />
            </div>
            <div className="uk-width-1-6@l uk-width-1-2@s">
                <input className="uk-input" type="number"  placeholder="от 4000 сом"
                value={this.props.priceTo} onChange={this.handlePriceToChange}/>
            </div>
            <div className="uk-width-1-3@l uk-width-1-2@s">
                <input className="uk-input" type="text" placeholder="Поиск товара" onChange={this.search}/>
            </div>
        </form>

    )
  }
});

module.exports=SearchForm;
