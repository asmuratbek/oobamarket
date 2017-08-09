import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/Product';
import _ from 'lodash';
import Pagination from 'react-js-pagination';
import Loader from 'react-loader';
import $ from 'jquery';



var MainInterface = createClass({
    displayName: 'MainInterface',

    getInitialState: function () {
        return {
            products: [],
            activePage: 1,
            loaded: false,
            activeCategories: [],
            categorySlug: location.href.split("/")[location.href.split("/").length - 2]
        }
    },

    componentDidMount() {
        var params = location.search.substr(1).split("&")
        params.forEach(function (i) {
            if (i.split("=")[0] == "q") {
                this.setState({
                    queryText: i.split("=")[1].toLowerCase()
                })
            }
        }.bind(this));

        $.ajax({
            type: "GET",
              url: `/api/v1/product/`,
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
              url: this.state.baseUrl + '?page=' + pageNumber,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    this.setState({
                        products: products,
                        activePage: pageNumber,
                        loaded: true
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

    render: function () {
        var allProducts = this.state.products;
        var productDelete = this.productDelete;
        var filteredProducts = [];

        filteredProducts = allProducts.map(function (item, index) {
            return (
                <Product key={ index }
                         onProductDelete={productDelete}
                         product={ item }/>
            ) //return
        }.bind(this));

        return (
            <div>
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


