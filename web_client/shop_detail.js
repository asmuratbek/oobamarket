import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/ShopDetailProducts';
import SearchForm from './components/ShopDetailSearchForm';
import CategoryList from './components/ShopDetailCategory';
import ProductsCount from './components/ProductsCount';
import axios from 'axios';
import _ from 'lodash';
import AlertContainer from 'react-alert';
import Alert from './components/Alert';


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
      products: [],
      categories: [],
      activeCategories: [],
      shopSlug : location.href.split("/")[4]
    }
  },

  componentDidMount() {
  axios.get(`/product/api/?shop=` + this.state.shopSlug)
    .then(res => {
      var products = res.data.map(obj => obj);
      this.setState({
         products: products,
       });
    });

    axios.get(`/api/category/shop/` + this.state.shopSlug)
      .then(res => {
        var categories = res.data.map(obj => obj);
        this.setState({
           categories: categories
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
  productDelete: function(item) {
    var allProducts = this.state.products;
    var deleted = _.remove(allProducts, function(n) {
      return n.id == item;
    });
    var newProducts = _.without(allProducts, deleted);
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

  changeCategory(title) {
    var activeCategories = this.state.activeCategories;
    if (activeCategories.indexOf(title)!=-1) {
      activeCategories = _.without(activeCategories, title);
    }
    else {
      activeCategories.push(title);
    }
    this.setState({
      activeCategories: activeCategories
    })
  },


  render: function() {
    var filteredProducts = [];
    var filteredShops = [];
    var categories = [];
    var shopTitles = [];
    var allProducts = this.state.products;
    var orderBy = this.state.orderBy;
    var queryText = this.state.queryText;
    var orderDir = this.state.orderDir;
    var deliveryType = this.state.deliveryType;
    var changeCategory = this.changeCategory;
    var activeCategories = this.state.activeCategories;
    var productDelete = this.productDelete;

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

    if (this.state.activeCategories.length > 0){
      filteredProducts = _.filter(filteredProducts, function(item){
        return _.indexOf(this.state.activeCategories, item.category_title)!=-1
      }.bind(this));
    };

    filteredProducts = filteredProducts.map(function(item, index) {
      shopTitles.push(item.shop);
      return(
        <Product key = { index }
          onProductDelete={productDelete}
          product = { item } />
      ) //return
    }.bind(this));

    shopTitles = _.uniqBy(shopTitles, function(e){
       return e;
    });

    filteredShops = _.filter(this.state.shops, function(item){
      return shopTitles.indexOf(item.title)!=-1
    });

    categories = this.state.categories.map(function(item, index) {
      return (
        <CategoryList
          key={index}
          category={item}
          onChangeCategory={changeCategory}
          activeCategories={activeCategories}
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
      <div className="col-md-3">
        <ul>

        <li>Все категории</li>
                {categories}
        </ul>
    </div>
    <div className="col-md-9">
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
       <div className="col-md-4 col-sm-6">
            <div className="cover">
                <a className="url-item" href={`/product/${this.state.shopSlug}/add-product/`}></a>
                <div className="add-product">
                    <i className="glyphicon glyphicon-plus-sign"></i>
                    <p>Добавить новый товар</p>
                </div>

                <div className="stock">
                    <a href={`/shops/${this.state.shopSlug}/sale/create/`}>Добавить акцию</a>
                </div>
            </div>
        </div>
      {filteredProducts}
      </div>
      </div>
    )
  }
});

ReactDOM.render(<MainInterface />, document.getElementById('root'));
