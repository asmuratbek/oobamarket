import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/Product';
import SearchForm from './components/SearchForm';
import CategoryList from './components/CategoryList';
import ProductsCount from './components/ProductsCount';
import ShopList from './components/ShopList';
import axios from 'axios';
import _ from 'lodash';



var MainInterface = createClass({
  displayName: 'MainInterface',

  getInitialState: function(){
    return {
      orderBy: 'title',
      queryText: '',
      products: []
    }
  },

  componentDidMount() {
  axios.get(`http://localhost:8000/product/api/?limit=10`)
    .then(res => {
      const products = res.data.results.map(obj => obj);
      this.setState({
         products: products
       });
    });
  },

  deleteMessage: function(item) {
    var allProducts = this.state.products;
    var newProducts = _.without(allProducts, item);
    this.setState({
      products: newProducts
    }); //setState
  },

  reOrder: function(orderBy) {
    this.setState({
      orderBy: orderBy,
    }); //setState
  }, //reOrder

  searchApts(q) {
    this.setState({
      queryText: q
    }); //setState
  }, //searchApts


  render: function() {
    var filteredProducts = [];
    var allProducts = this.state.products;
    var orderBy = this.state.orderBy;
    var queryText = this.state.queryText;


    allProducts.forEach(function(item) {
      if(item.title.toLowerCase().indexOf(queryText)!=-1)
      {
        filteredProducts.push(item);
      }
    });

    filteredProducts = filteredProducts.map(function(item, index) {
      return(
        <Product key = { index }
          product = { item } />
      ) //return
    }.bind(this));

    filteredProducts = _.orderBy(filteredProducts, function(item) {
      console.log(filteredProducts)
      console.log(item)
      console.log(item.props.product.title)
      return item.title;
    }, 'desc');//orderBy



    return (
      <div>
      <ShopList />
      <ProductsCount />
      <CategoryList />
      <SearchForm
          orderBy = { this.state.orderBy }
          onReOrder = { this.reOrder }
          onSearch = { this.searchApts }
       />
      {filteredProducts}
      </div>
    )
  }
});

ReactDOM.render(<MainInterface />, document.getElementById('root'));
