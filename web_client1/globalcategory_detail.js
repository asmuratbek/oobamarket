import React from "react";
import ReactDOM from "react-dom";
import createClass from "create-react-class";
import Product from "./components/Product";
import SearchForm from "./components/SearchForm";
import _ from "lodash";
import Pagination from "react-js-pagination";
import $ from "jquery";


var MainInterface = createClass({
    displayName: 'MainInterface',

    getInitialState: function () {
        return {
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
            domain: location.href.split("/")[2].split(":")[0],
            categorySlug: location.href.split("/")[location.href.split("/").length - 2]
        }
    },

    componentDidMount() {
        const params = location.search.substr(1).split("&")
        params.forEach(function (i) {
            if (i.split("=")[0] == "q") {
                this.setState({
                    queryText: i.split("=")[1]
                })
            }
        }.bind(this));

        const elasticsearch = require('elasticsearch');
        const client = new elasticsearch.Client({
          host: 'localhost:9200',
          log: 'trace'
        });

        const query = {
                'query': {
                    'match_phrase': {
                        'global_slug': this.state.categorySlug
                    }
                },
                "size":  this.state.productsByPage,
                "from": 0,
                "sort": [
                    {"created_at": "desc"},
                ]
              };
        client.search({
              query
            }).then(function (data) {
                const products = data.hits.hits.map(obj => obj._source);
                const pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                this.setState({
                    products: products,
                    productsCount: data.hits.total,
                    activePage: 1,
                    pagesCount: pagesCount,
                    loaded: true
                });
            }, function (err) {
                console.trace(err.message);
            });

        fetch(`http://${this.state.domain}:8000/api/v1/my-list/`)
          .then(function(data) {
                const favorites = data.favorites.map(obj => obj.id);
                const cartItems = data.cart_items.map(obj => obj.id);
                this.setState({
                    favorites: favorites,
                    cartItems: cartItems
                });
          })
    },

    handlePageChange: function(pageNumber) {
        var from = this.state.productsCount > this.state.productsByPage * pageNumber ? (
            this.state.productsByPage * pageNumber
        ) : (
            this.state.activePage * this.state.productsByPage
        );
        if (this.state.orderBy == '-created_at') {
            var sort = {'created_at': 'desc'}
        } else if (this.state.orderBy == 'title'){
            var sort = {'title': 'asc'}
        } else if (this.state.orderBy == 'price') {
            var sort = {'get_price_function': 'asc'}
        } else if (this.state.orderBy == '-price') {
            var sort = {'get_price_function': 'desc'}
        }

        if (this.state.priceFrom && this.state.priceTo) {
            var sorting = [{"range": {"get_price_function": {"gte": this.state.priceFrom}}},
                {"range": {"get_price_function": {"lte": this.state.priceTo}}}]
        } else if (this.state.priceFrom) {
            var sorting = [
                {"range": {"get_price_function": {"gte": this.state.priceFrom}}}
            ]
        } else if (this.state.priceTo) {
            var sorting = [
                {"range": {"get_price_function": {"lte": this.state.priceTo}}}
            ]
        }
        if (this.state.queryText) {
            var q = [
                { "match": { "text":  this.state.queryText }},
                { "match_phrase": { "global_slug":  this.state.categorySlug }},
            ]
        } else {
            var q = [
                { "match_phrase": { "global_slug":  this.state.categorySlug }}
            ]
        }
        var query = {
                'query': {
                        "bool": {
                            "must": q,
                            "filter": sorting
                        }

                      },
                "size":  this.state.productsByPage,
                "from": pageNumber == 1 ? 0 : from,
                "sort": [
                    sort,
                ],
              };
        this.setState({
           loaded: false
        });
        $.ajax({
             type: "POST",
              url: `http://${this.state.domain}:9200/_search/`,
              data: JSON.stringify(query),
              contentType: 'application/json',
              dataType : 'json',
              success: function (data) {
                    var products = data.hits.hits.map(obj => obj._source);
                    this.setState({
                        products: products,
                        activePage: pageNumber,
                        loaded: true,
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    },

    deleteMessage: function (item) {
        var allProducts = this.state.products;
        var newProducts = _.without(allProducts, item);
        this.setState({
            products: newProducts
        }); //setState
    },
    productDelete: function (item) {
        var allProducts = this.state.products;
        var deleted = _.remove(allProducts, function (n) {
            return n.id == item;
        });
        var newProducts = _.without(allProducts, deleted);
        this.setState({
            products: newProducts
        }); //setState
    },


    reOrder: function (orderBy) {
        console.log(orderBy)
        var from = this.state.activePage * this.state.productsByPage;
        if (orderBy == '-created_at') {
            var sort = {'created_at': 'desc'}
        } else if (orderBy == 'title'){
            var sort = {'title': 'asc'}
        } else if (orderBy == 'price') {
            var sort = {'get_price_function': 'asc'}
        } else if (orderBy == '-price') {
            var sort = {'get_price_function': 'desc'}
        }
        console.log(sort)
        if (this.state.priceFrom && this.state.priceTo) {
            var sorting = [{"range": {"get_price_function": {"gte": this.state.priceFrom}}},
                {"range": {"get_price_function": {"lte": this.state.priceTo}}}]
        } else if (this.state.priceFrom) {
            var sorting = [
                {"range": {"get_price_function": {"gte": this.state.priceFrom}}}
            ]
        } else if (this.state.priceTo) {
            var sorting = [
                {"range": {"get_price_function": {"lte": this.state.priceTo}}}
            ]
        }
        if (this.state.queryText) {
            var q = [
                {"match": {"text": this.state.queryText}},
                {"match_phrase": {"global_slug": this.state.categorySlug}},
            ]
        } else {
            var q = [
                { "match_phrase": { "global_slug":  this.state.categorySlug }}
            ]
        }
        var query = {
                'query': {
                        "bool": {
                            "must": q,
                            "filter": sorting
                        }

                      },
                "size":  this.state.productsByPage,
                "from": this.state.activePage == 1 ? 0 : from,
                "sort": [
                    sort,
                ],
              };
        this.setState({
           loaded: false
        });
        $.ajax({
           type: "POST",
              url: `http://${this.state.domain}:9200/_search/`,
              data: JSON.stringify(query),
              contentType: 'application/json',
              dataType : 'json',
              success: function (data) {
                    var products = data.hits.hits.map(obj => obj._source);
                    this.setState({
                        products: products,
                        loaded: true,
                        orderBy: orderBy
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })

    },

    searchApts(q) {
        var from = this.state.activePage * this.state.productsByPage;
        if (this.state.orderBy == '-created_at') {
            var sort = {'created_at': 'desc'}
        } else if (this.state.orderBy == 'title'){
            var sort = {'title': 'asc'}
        } else if (this.state.orderBy == 'price') {
            var sort = {'get_price_function': 'asc'}
        } else if (this.state.orderBy == '-price') {
            var sort = {'get_price_function': 'desc'}
        }

        if (this.state.priceFrom && this.state.priceTo) {
            var sorting = [{"range": {"get_price_function": {"gte": this.state.priceFrom}}},
                {"range": {"get_price_function": {"lte": this.state.priceTo}}}]
        } else if (this.state.priceFrom) {
            var sorting = [
                {"range": {"get_price_function": {"gte": this.state.priceFrom}}}
            ]
        } else if (this.state.priceTo) {
            var sorting = [
                {"range": {"get_price_function": {"lte": this.state.priceTo}}}
            ]
        }
        if (q) {
            var queryset = [
                {"match": {"text": q}},
                {"match_phrase": {"global_slug": this.state.categorySlug}},
            ]
        } else {
            var queryset = [
                { "match_phrase": { "global_slug":  this.state.categorySlug }}
            ]
        }
        var query = {
                'query': {
                        "bool": {
                            "must": queryset,
                            "filter": sorting
                        }

                      },
                "size":  this.state.productsByPage,
                "from": 0,
                "sort": [
                    sort,
                ],
              };
        this.setState({
            loaded: false,
        });
        $.ajax({
            type: "POST",
              url: `http://${this.state.domain}:9200/_search/`,
              data: JSON.stringify(query),
              contentType: 'application/json',
              dataType : 'json',
              success: function (data) {
                    var products = data.hits.hits.map(obj => obj._source);
                    var pagesCount = Math.ceil(data.hits.total / 20);
                    this.setState({
                        products: products,
                        loaded: true,
                        pagesCount: pagesCount,
                        productsCount: data.hits.total,
                        queryText: q,
                        activePage: 1
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    }, //searchApts

    changePriceFrom(price) {
        var from = this.state.activePage * this.state.productsByPage;
        if (this.state.orderBy == '-created_at') {
            var sort = {'created_at': 'desc'}
        } else if (this.state.orderBy == 'title'){
            var sort = {'title': 'asc'}
        } else if (this.state.orderBy == 'price') {
            var sort = {'get_price_function': 'asc'}
        } else if (this.state.orderBy == '-price') {
            var sort = {'get_price_function': 'desc'}
        }

        if (price && this.state.priceTo) {
            var sorting = [{"range": {"get_price_function": {"gte": parseInt(price)}}},
                {"range": {"get_price_function": {"lte": this.state.priceTo}}}]
        } else if (price) {
            var sorting = [
                {"range": {"get_price_function": {"gte": parseInt(price)}}}
            ]
        } else if (this.state.priceTo) {
            var sorting = [
                {"range": {"get_price_function": {"lte": this.state.priceTo}}}
            ]
        }
        if (this.state.queryText) {
            var q = [
                {"match": {"text": this.state.queryText}},
                {"match_phrase": {"global_slug": this.state.categorySlug}},
            ]
        } else {
            var q = [
                { "match_phrase": { "global_slug":  this.state.categorySlug }}
            ]
        }
        var query = {
                'query': {
                        "bool": {
                            "must": q,
                            "filter": sorting
                        }

                      },
                "size":  this.state.productsByPage,
                "from": 0,
                "sort": [
                    sort,
                ],
              };
        this.setState({
            loaded: false,

        });
        $.ajax({
           type: "POST",
              url: `http://${this.state.domain}:9200/_search/`,
              data: JSON.stringify(query),
              contentType: 'application/json',
              dataType : 'json',
              success: function (data) {
                    var products = data.hits.hits.map(obj => obj._source);
                    var pagesCount = Math.ceil(data.hits.total / 20);
                    this.setState({
                        products: products,
                        loaded: true,
                        priceFrom: parseInt(price),
                        pagesCount: pagesCount,
                        productsCount: data.hits.total,
                        activePage: 1
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    },

    changePriceTo(price) {
        var from = this.state.activePage * this.state.productsByPage;
        if (this.state.orderBy == '-created_at') {
            var sort = {'created_at': 'desc'}
        } else if (this.state.orderBy == 'title'){
            var sort = {'title': 'asc'}
        } else if (this.state.orderBy == 'price') {
            var sort = {'get_price_function': 'asc'}
        } else if (this.state.orderBy == '-price') {
            var sort = {'get_price_function': 'desc'}
        }

        if (price && this.state.priceFrom) {
            var sorting = [{"range": {"get_price_function": {"gte": this.state.priceFrom}}},
                {"range": {"get_price_function": {"lte": parseInt(price)}}}]
        } else if (this.state.priceFrom) {
            var sorting = [
                {"range": {"get_price_function": {"gte": this.state.priceFrom}}}
            ]
        } else if (price) {
            var sorting = [
                {"range": {"get_price_function": {"lte": parseInt(price)}}}
            ]
        }
        if (this.state.queryText) {
            var q = [
                {"match": {"text": this.state.queryText}},
                {"match_phrase": {"global_slug": this.state.categorySlug}},
            ]
        } else {
            var q = [
                { "match_phrase": { "global_slug":  this.state.categorySlug }}
            ]
        }
        var query = {
                'query': {
                        "bool": {
                            "must": q,
                            "filter": sorting
                        }

                      },
                "size":  this.state.productsByPage,
                "from": 0,
                "sort": [
                    sort,
                ],
              };
        this.setState({
            loaded: false
        });
        $.ajax({
            type: "POST",
              url: `http://${this.state.domain}:9200/_search/`,
              data: JSON.stringify(query),
              contentType: 'application/json',
              dataType : 'json',
              success: function (data) {
                    var products = data.hits.hits.map(obj => obj._source);
                    var pagesCount = Math.ceil(data.hits.total / 20);
                    this.setState({
                        products: products,
                        loaded: true,
                        priceTo: parseInt(price),
                        pagesCount: pagesCount,
                        productsCount: data.hits.total,
                        activePage: 1
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    },


    render: function () {
        var filteredProducts = [];
        var productDelete = this.productDelete;

        filteredProducts = this.state.products.map(function (item, index) {
            return (
                <Product key={ index }
                         onProductDelete={productDelete}
                         favorites={this.state.favorites}
                         cartItems={this.state.cartItems}
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
                  itemsCountPerPage={20}
                  totalItemsCount={this.state.productsCount}
                  pageRangeDisplayed={5}
                  onChange={this.handlePageChange}
                />
                : ''}
            </div>
        )
    }
});


ReactDOM.render(<MainInterface />, document.getElementById('root'));

