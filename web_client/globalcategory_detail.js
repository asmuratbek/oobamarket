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
        return {
            orderBy: '-created_at',
            priceFrom: '',
            priceTo: '',
            queryText: '',
            products: [],
            activePage: 1,
            shops: [],
            categories: [],
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
              url: `/api/v1/globalcategory/` + this.state.categorySlug + '/?ordering=' + this.state.orderBy,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 20);
                    this.setState({
                        products: products,
                        productsCount: data.count,
                        activePage: 1,
                        pagesCount: pagesCount,
                        baseUrl: `/api/v1/globalcategory/` + this.state.categorySlug + '/',
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
              url: this.state.baseUrl + '?ordering=' + this.state.orderBy + '&page=' + pageNumber,
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
              url: this.state.baseUrl + '?ordering=' + orderBy + '&page=' + this.state.activePage,
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

        // this.setState({
        //     orderBy: orderBy,
        //     orderDir: orderDir
        // }); //setState
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
        if (activeCategories.indexOf(title) != -1) {
            activeCategories = _.without(activeCategories, title);
        }
        else {
            activeCategories.push(title);
        }
        this.setState({
            activeCategories: activeCategories
        })
    },


    render: function () {
        var filteredProducts = [];
        var categories = [];
        var allProducts = this.state.products;
        var orderBy = this.state.orderBy;
        var queryText = this.state.queryText;
        var orderDir = this.state.orderDir;
        var deliveryType = this.state.deliveryType;
        var changeCategory = this.changeCategory;
        var activeCategories = this.state.activeCategories;
        var productDelete = this.productDelete;

        allProducts.forEach(function (item) {
            if (item.title.toLowerCase().indexOf(queryText) != -1) {
                    filteredProducts.push(item);
            }
        });

        if (this.state.priceFrom > 0) {
            filteredProducts = _.filter(filteredProducts, function (item) {
                return item.price > parseInt(this.state.priceFrom)
            }.bind(this));
        }
        ;

        if (this.state.priceTo > 0) {
            filteredProducts = _.filter(filteredProducts, function (item) {
                return item.price < parseInt(this.state.priceTo)
            }.bind(this));
        }
        ;

        if (this.state.activeCategories.length > 0) {
            filteredProducts = _.filter(filteredProducts, function (item) {
                return _.indexOf(this.state.activeCategories, item.category_title) != -1
            }.bind(this));
        }
        ;

        filteredProducts = filteredProducts.map(function (item, index) {
            return (
                <Product key={ index }
                         onProductDelete={productDelete}
                         product={ item }/>
            ) //return
        }.bind(this));


        categories = this.state.categories.map(function (item, index) {
            return (
                <CategoryList
                    key={index}
                    category={item}
                    onChangeCategory={changeCategory}
                    activeCategories={activeCategories}
                />
            )
        });


        return (
            <div>

                <ul className="category-tab">
                    {categories}
                </ul>
                <SearchForm
                    orderBy={ this.state.orderBy }
                    onReOrder={ this.reOrder }
                    onSearch={ this.searchApts }
                    priceFrom={ this.state.priceFrom }
                    priceTo={ this.state.priceTo }
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

