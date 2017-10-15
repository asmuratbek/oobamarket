import React, { Component } from 'react';
import urlmaker from './urlmaker';
import Product from './components/Product';
import SearchForm from './components/SearchFrom';
import Pagination from 'react-js-pagination';
import $ from 'jquery';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
        orderBy: '-created_at',
        priceFrom: '',
        priceTo: '',
        queryText: '',
        products: [],
        activePage: 1,
        shops: [],
        favorites: [],
        cartItems: [],
        categories: [],
        loaded: false,
        activeCategories: [],
        productsByPage: 20,
        domain: window.location.href.split("/")[2].split(":")[0],
        categorySlug: window.location.href.split("/")[window.location.href.split("/").length - 2]
    }
  }

  componentDidMount = () => {
        const params = window.location.search.substr(1).split("&");
        params.forEach(function (i) {
            if (i.split("=")[0] === "q") {
                this.setState({
                    queryText: i.split("=")[1]
                })
            }
        }.bind(this));

        const query = {
                query: {
                    match_phrase: {
                        global_slug: this.state.categorySlug
                    }
                },
                size:  this.state.productsByPage,
                from: 0,
                sort: [
                    {created_at: "desc"},
                ]
              };

        // fetch(`http://${this.state.domain}:8000/api/v1/my-list/`, {
        //     method: "GET"
        // })
        //     .then(function(res) {
        //         return res.json();
        //     }).then(function(data) {
        //         const favorites = data.favorites.map(obj => obj.id);
        //         const cartItems = data.cart_items.map(obj => obj.id);
        //         this.setState({
        //             favorites: favorites,
        //             cartItems: cartItems
        //         });
        //     }.bind(this));

      $.ajax({
            type: "GET",
              url: `http://${this.state.domain}:8000/api/v1/my-list/`,
              success: function (data) {
                    let favorites = data.favorites.map(obj => obj.id);
                    let cartItems = data.cart_items.map(obj => obj.id);
                    let shops = data.shops.map(obj => obj.title);
                    this.setState({
                        favorites: favorites,
                        cartItems: cartItems,
                        shops: shops
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })

        fetch(`http://${this.state.domain}:9200/_search/`, {
            method: "POST",
            body: JSON.stringify(query)
        }).then(function(res) {
                return res.json();
            }).then(function(data) {
                const products = data.hits.hits.map(obj => obj._source);
                const pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                this.setState({
                    products: products,
                    productsCount: data.hits.total,
                    activePage: 1,
                    pagesCount: pagesCount,
                    loaded: true
                });
            }.bind(this));
  };

  handlePageChange = (pageNumber) => {
        this.setState({
           loaded: false
        });

        let query = urlmaker(this.state.productsCount, this.state.productsByPage, pageNumber,
                            this.state.activePage, this.state.orderBy, this.state.priceFrom,
                            this.state.priceTo, this.state.queryText, this.state.categorySlug);

      fetch(`http://${this.state.domain}:9200/_search/`, {
            method: "POST",
            body: JSON.stringify(query)
        }).then(function(res) {
                return res.json();
            }).then(function (data) {
                const products = data.hits.hits.map(obj => obj._source);
                this.setState({
                    products: products,
                    activePage: pageNumber,
                    loaded: true,
                });
            }.bind(this), function (err) {
                console.trace(err.message);
            });
  };

  reOrder = (orderBy) => {
      this.setState({
           loaded: false
        });

        let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            this.state.activePage, orderBy, this.state.priceFrom,
                            this.state.priceTo, this.state.queryText, this.state.categorySlug);

      fetch(`http://${this.state.domain}:9200/_search/`, {
            method: "POST",
            body: JSON.stringify(query)
        }).then(function(res) {
                return res.json();
            }).then(function (data) {
                const products = data.hits.hits.map(obj => obj._source);
                this.setState({
                    products: products,
                    orderBy: orderBy,
                    loaded: true,
                });
            }.bind(this), function (err) {
                console.trace(err.message);
            });
  };

  searchApts = (q) => {
      this.setState({
           loaded: false
        });

        let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            this.state.activePage, this.state.orderBy, this.state.priceFrom,
                            this.state.priceTo, q, this.state.categorySlug);

      fetch(`http://${this.state.domain}:9200/_search/`, {
            method: "POST",
            body: JSON.stringify(query)
        }).then(function(res) {
                return res.json();
            }).then(function (data) {
                let products = data.hits.hits.map(obj => obj._source);
                let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                this.setState({
                    products: products,
                    loaded: true,
                    pagesCount: pagesCount,
                    productsCount: data.hits.total,
                    queryText: q,
                    activePage: 1
                });
            }.bind(this), function (err) {
                console.trace(err.message);
            });
  };

  changePriceFrom = (price) => {
      this.setState({
           loaded: false
        });

        let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            this.state.activePage, this.state.orderBy, price,
                            this.state.priceTo, this.state.queryText, this.state.categorySlug);

      fetch(`http://${this.state.domain}:9200/_search/`, {
            method: "POST",
            body: JSON.stringify(query)
        }).then(function(res) {
                return res.json();
            }).then(function (data) {
                let products = data.hits.hits.map(obj => obj._source);
                let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                this.setState({
                    products: products,
                    loaded: true,
                    priceFrom: parseInt(price, 10),
                    pagesCount: pagesCount,
                    productsCount: data.hits.total,
                    activePage: 1
                });
            }.bind(this), function (err) {
                console.trace(err.message);
            });
  };

  changePriceTo = (price) => {
      this.setState({
           loaded: false
        });

        let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            this.state.activePage, this.state.orderBy, this.state.priceFrom,
                            price, this.state.queryText, this.state.categorySlug);

      fetch(`http://${this.state.domain}:9200/_search/`, {
            method: "POST",
            body: JSON.stringify(query)
        }).then(function(res) {
                return res.json();
            }).then(function (data) {
                let products = data.hits.hits.map(obj => obj._source);
                let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                this.setState({
                    products: products,
                    loaded: true,
                    priceTo: parseInt(price, 10),
                    pagesCount: pagesCount,
                    productsCount: data.hits.total,
                    activePage: 1
                });
            }.bind(this), function (err) {
                console.trace(err.message);
            });
  };

  render() {
        let filteredProducts = [];
        let productDelete = this.productDelete;

        filteredProducts = this.state.products.map(function (item, index) {
            return (
                <Product key={ index }
                         onProductDelete={productDelete}
                         favorites={this.state.favorites}
                         cartItems={this.state.cartItems}
                         shops={this.state.shops}
                         product={ item }/>
            ) //return
        }.bind(this));


        return (
            <div className="uk-container">
                <SearchForm
                    orderBy={ this.state.orderBy }
                    onReOrder={ this.reOrder }
                    onSearch={ this.searchApts }
                    priceFrom={ this.state.priceFrom }
                    priceTo={ this.state.priceTo }
                    query={this.state.queryText}
                    onChangePriceFrom={ this.changePriceFrom }
                    onChangePriceTo={ this.changePriceTo }
                />

                <div className="uk-child-width-1-1 uk-child-width-1-2@s uk-child-width-1-3@m  uk-child-width-1-4@l uk-grid-small" data-uk-grid>

                    {filteredProducts}

                </div>

                {this.state.pagesCount > 1 ?
                <Pagination
                  activePage={this.state.activePage}
                  itemsCountPerPage={this.state.productsByPage}
                  totalItemsCount={this.state.productsCount}
                  pageRangeDisplayed={5}
                  onChange={this.handlePageChange}
                />
                : ''}
            </div>
        )
  }
}

export default App;
