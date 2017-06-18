import React from 'react';
import createClass from 'create-react-class';


var SearchForm = createClass({
  displayName: 'SearchForm',

  handleSort: function(e) {
    this.props.onReOrder(e.target.value);
  }, //handleSort

  render: function(){
    return (
      <div className="form-filter">
                <form className="form-inline">

                    <div className="form-group select">
                        <select className="form-control" value={this.props.orderBy} onChange={this.handleSort}>
                            <option value="title">По названию</option>
                            <option value="priceAsc">Цена по возрастанию</option>
                            <option value="priceDesc">Цена по убыванию </option>
                            <option value="newFirst">Сначала новые </option>
                        </select>
                    </div>

                    <div className="form-group input">
                        <label><span>Цена</span> от</label>
                        <input type="text" className="form-control" placeholder="2000 сом" />
                    </div>

                    <div className="form-group input end">
                        <label>до</label>
                        <input type="text" className="form-control" placeholder="4000 сом" />
                    </div>

                     <div className="form-group select">
                        <select className="form-control">
                            <option>Доставка</option>
                            <option>Бесплатная</option>
                            <option>Платная</option>
                            <option>Самовывоз</option>
                        </select>
                    </div>

                    <div className="form-group search">
                        <button type="submit" className="btn btn-default"> ПОКАЗАТЬ</button>
                    </div>

                </form>
            </div>
    )
  }
});

module.exports=SearchForm;
