import React, { Component } from 'react';
import client from './elasticconfig';
import urlmaker from './urlmaker';

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
        this.setState({
           loaded: false
        });

        var query = urlmaker(this.state.productsCount, this.state.productsByPage, pageNumber,
                            this.state.activePage, this.state.orderBy, this.state.priceFrom,
                            this.state.priceTo, this.state.queryText, this.state.categorySlug);

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
