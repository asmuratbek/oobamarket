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
      orderDir: 'asc',
      priceFrom: '',
      priceTo: '',
      queryText: '',
      deliveryType: 'all',
      productsCount: 0,
      products: [],
      shops: []
    }
  },

  componentDidMount() {
    var params = location.search.substr(1).split("&")
    params.forEach(function(i){
      if (i.split("=")[0] == "q"){
        this.setState({
          queryText: i.split("=")[1].toLowerCase()
        })
      }
    }.bind(this));
  axios.get(`/product/api/`)
    .then(res => {
      const products = res.data.map(obj => obj);
      this.setState({
         products: products
       });
    });
  axios.get(`/shops/api/`)
      .then(res => {
        const shops = res.data.map(obj => obj);
        this.setState({
          shops: shops
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

  reOrder: function(orderBy, orderDir) {
    this.setState({
      orderBy: orderBy,
      orderDir: orderDir
    }); //setState
  }, //reOrder

  changeDeliveryType: function(deliveryType) {
    this.setState({
      deliveryType: deliveryType
    });
  },

  searchApts(q) {
    this.setState({
      queryText: q.toLowerCase()
    }); //setState
  }, //searchApts

  changePriceFrom(price) {
    this.setState({
      priceFrom: parseInt(price)
    })
  },

  changePriceTo(price) {
    this.setState({
      priceTo: parseInt(price)
    })
  },


  render: function() {
    var filteredProducts = [];
    var categories = [];
    var allProducts = this.state.products;
    var orderBy = this.state.orderBy;
    var queryText = this.state.queryText;
    var orderDir = this.state.orderDir;
    var deliveryType = this.state.deliveryType;

    allProducts.forEach(function(item) {
      if(item.title.toLowerCase().indexOf(queryText)!=-1)
      {
        if (item.delivery_type == deliveryType || deliveryType == 'all'){
          filteredProducts.push(item);
        }
      }
    });

    if (this.state.priceFrom > 0) {
      filteredProducts = _.filter(filteredProducts, function(item){
        return item.price > parseInt(this.state.priceFrom)
      }.bind(this));
    };

    if (this.state.priceTo > 0) {
      filteredProducts = _.filter(filteredProducts, function(item){
        return item.price < parseInt(this.state.priceTo)
      }.bind(this));
    };

    filteredProducts = filteredProducts.map(function(item, index) {
      categories.push(item.get_category_title);
      return(
        <Product key = { index }
          product = { item } />
      ) //return
    }.bind(this));

    categories = _.uniqBy(categories, function (e) {
          return e;
    });

    categories = categories.map(function(item, index) {
      return (
        <CategoryList
          key={index}
          category={item}
        />
      )
    });



    var productsCount = filteredProducts.length

    filteredProducts = _.orderBy(filteredProducts, function(item) {
      if (orderBy == 'title'){
          return item.props.product.title.toLowerCase();
      }
      else if (orderBy == 'priceAsc') {
          return item.props.product.get_price_function;
      }
      else if (orderBy == 'priceDesc') {
          return item.props.product.get_price_function;
      }
      else if (orderBy == 'newFirst') {
          return item.props.product.created_at;
      }
    }, orderDir);//orderBy



    return (
      <div>
      <ShopList
        shops = { this.state.shops }
        q = { this.state.queryText }
      />
      <ProductsCount
        count = {productsCount}
      />
      <ul className="category-tab">
      {categories}
      </ul>
      <SearchForm
          orderBy = { this.state.orderBy }
          onReOrder = { this.reOrder }
          onSearch = { this.searchApts }
          deliveryType = { this.state.deliveryType }
          onChangeDeliveryType = { this.changeDeliveryType }
          priceFrom = { this.state.priceFrom }
          priceTo = { this.state.priceTo }
          onChangePriceFrom = { this.changePriceFrom }
          onChangePriceTo = { this.changePriceTo }
       />
      {filteredProducts}
      </div>
    )
  }
});

ReactDOM.render(<MainInterface />, document.getElementById('root'));
