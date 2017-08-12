import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/Product';
import SearchForm from './components/SearchForm';
import CategoryList from './components/CategoryList';
import _ from 'lodash';
import Pagination from 'react-js-pagination';
import Loader from 'react-loader';


var MainInterface = createClass({
    displayName: 'MainInterface',

    getInitialState: function () {
        var parseQueryString = function () {

        var str = location.search;
        var objURL = {};

        str.replace(
            new RegExp("([^?=&]+)(=([^&]*))?", "g"),
            function ($0, $1, $2, $3) {
                objURL[$1] = $3;
            }
        );
        return objURL;
    };

        //Example how to use it:
        var params = parseQueryString();
        return {
            orderBy: '-created_at',
            priceFrom: '',
            priceTo: '',
            products: [],
            queryText: params['q'] ? decodeURIComponent(params['q']) : '',
            activePage: 1,
            shops: [],
            categories: [],
            loaded: false,
            activeCategories: [],
        }
    },

    componentDidMount() {
        $.ajax({
            type: "GET",
              url: `/api/v1/product/` + '?ordering=' + this.state.orderBy + '&page=' + this.state.activePage +
              '&priceFrom=' + this.state.priceFrom + '&priceTo=' + this.state.priceTo + '&q=' + this.state.queryText,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 20);
                    this.setState({
                        products: products,
                        productsCount: data.count,
                        activePage: 1,
                        pagesCount: pagesCount,
                        baseUrl: `/api/v1/product/`,
                        loaded: true
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    },

    handlePageChange: function(pageNumber) {
        this.setState({
           loaded: false
        });
        $.ajax({
            type: "GET",
              url: this.state.baseUrl + '?ordering=' + this.state.orderBy + '&page=' + pageNumber +
              '&priceFrom=' + this.state.priceFrom + '&priceTo=' + this.state.priceTo + '&q=' + this.state.queryText,
              success: function (data) {
                    var products = data.results.map(obj => obj);
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
        this.setState({
           loaded: false
        });
        $.ajax({
            type: "GET",
              url: this.state.baseUrl + '?ordering=' + orderBy + '&page=' + this.state.activePage +
              '&priceFrom=' + this.state.priceFrom + '&priceTo=' + this.state.priceTo + '&q=' + this.state.queryText,
              success: function (data) {
                    var products = data.results.map(obj => obj);
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
        this.setState({
            loaded: false,
        });
        $.ajax({
            type: "GET",
              url: this.state.baseUrl + '?ordering=' + this.state.orderBy + '&page=1' +
              '&priceFrom=' + this.state.priceFrom + '&priceTo=' + this.state.priceTo +
              '&q=' + q.toLowerCase(),
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 20);
                    this.setState({
                        products: products,
                        loaded: true,
                        pagesCount: pagesCount,
                        productsCount: data.count,
                        queryText: q.toLowerCase(),
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
        this.setState({
            loaded: false,

        });
        $.ajax({
            type: "GET",
              url: this.state.baseUrl + '?ordering=' + this.state.orderBy + '&page=1' +
              '&priceFrom=' + parseInt(price) + '&priceTo=' + this.state.priceTo + '&q=' + this.state.queryText,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 20);
                    this.setState({
                        products: products,
                        loaded: true,
                        priceFrom: parseInt(price),
                        pagesCount: pagesCount,
                        productsCount: data.count,
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
        this.setState({
            loaded: false
        });
        $.ajax({
            type: "GET",
              url: this.state.baseUrl + '?ordering=' + this.state.orderBy + '&page=1' +
              '&priceFrom=' + this.state.priceFrom + '&priceTo=' + parseInt(price) + '&q=' + this.state.queryText,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 20);
                    this.setState({
                        products: products,
                        loaded: true,
                        priceTo: parseInt(price),
                        pagesCount: pagesCount,
                        productsCount: data.count,
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
                         product={ item }/>
            ) //return
        }.bind(this));


        return (
            <div>
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
                <div className="item-filter">
                    <Loader loaded={this.state.loaded}>
                    {filteredProducts}
                    <div className="clearfix"></div>
                    </Loader>
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

