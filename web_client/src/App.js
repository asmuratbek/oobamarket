import React, { Component } from 'react';
import client from './elasticconfig'

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

  componentWillMount = () => {
        const params = window.location.search.substr(1).split("&")
        params.forEach(function (i) {
            if (i.split("=")[0] === "q") {
                this.setState({
                    queryText: i.split("=")[1]
                })
            }
        }.bind(this));

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
            }.bind(this), function (err) {
                console.trace(err.message);
            });

        fetch(`http://${this.state.domain}:8000/api/v1/my-list/`)
            .then(function(res) {
                return res.json();
            }).then(function(data) {
                console.log(data);
                const favorites = data.favorites.map(obj => obj.id);
                const cartItems = data.cart_items.map(obj => obj.id);
                this.setState({
                    favorites: favorites,
                    cartItems: cartItems
                });
            }.bind(this));
  }

  handlePageChange = (pageNumber) => {
      var from = this.state.productsCount > this.state.productsByPage * pageNumber ? (
            this.state.productsByPage * pageNumber
        ) : (
            this.state.activePage * this.state.productsByPage
        );

      var sort = () => {
        if (this.state.orderBy === '-created_at') {
            return {'created_at': 'desc'}
        } else if (this.state.orderBy === 'title'){
            return {'title': 'asc'}
        } else if (this.state.orderBy === 'price') {
            return {'get_price_function': 'asc'}
        } else if (this.state.orderBy === '-price') {
            return {'get_price_function': 'desc'}
        }
      }

      var sorting = () => {
            if (this.state.priceFrom && this.state.priceTo) {
                return [{"range": {"get_price_function": {"gte": this.state.priceFrom}}},
                    {"range": {"get_price_function": {"lte": this.state.priceTo}}}]
            } else if (this.state.priceFrom) {
                return [
                    {"range": {"get_price_function": {"gte": this.state.priceFrom}}}
                ]
            } else if (this.state.priceTo) {
                return [
                    {"range": {"get_price_function": {"lte": this.state.priceTo}}}
                ]
            }
      }


      var q = () => {
        if (this.state.queryText) {
            return [
                { "match": { "text":  this.state.queryText }},
                { "match_phrase": { "global_slug":  this.state.categorySlug }},
            ]
        } else {
            return [
                { "match_phrase": { "global_slug":  this.state.categorySlug }}
            ]
        }
      }

        var query = {
                'query': {
                        "bool": {
                            "must": q,
                            "filter": sorting
                        }

                      },
                "size":  this.state.productsByPage,
                "from": pageNumber === 1 ? 0 : from,
                "sort": [
                    sort,
                ],
              };
        this.setState({
           loaded: false
        });

      client.search({
              query
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
  }

  render() {
    return (
      <div className="App">
        <h1>Heeey</h1>
      </div>
    );
  }
}

export default App;
