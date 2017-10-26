import React, {Component} from 'react';

class SearchForm extends Component {
  handleSort = (e) => {
      this.props.onReOrder(e.target.value);
  };

  handlePriceFromChange = (e) => {
    this.props.onChangePriceFrom(e.target.value)
  };

  handlePriceToChange = (e)=> {
    this.props.onChangePriceTo(e.target.value)
  };

  search =(e) => {
      let query = e.target.value;
      this.props.onSearch(query)
  };

  render () {
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
}

export default SearchForm;
