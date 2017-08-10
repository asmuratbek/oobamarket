import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/ShopDetailProducts';
import SearchForm from './components/SearchForm';
import CategoryList from './components/ShopDetailCategory';
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
            productsCount: 0,
            activePage: 1,
            pagesCount: 0,
            products: [],
            shops: [],
            loaded: false,
            categories: [],
            activeCategories: [],
            owner: false,
            shopSlug: location.href.split("/")[4]
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
              url: `/api/v1/shop/` + this.state.shopSlug + '/shop/',
              success: function (data) {
                   var owner = data[0].shop[0].is_owner;
                    var categories = data[1].category.map(obj =>obj);
                    this.setState({
                        owner: owner,
                        categories:categories,

                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })

        $.ajax({
            type: "GET",
              url: `/api/v1/shop/` + this.state.shopSlug + '?ordering=' + this.state.orderBy + '&page=' + this.state.activePage +
              '&priceFrom=' + this.state.priceFrom + '&priceTo=' + this.state.priceTo,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 21);
                    this.setState({
                        products: products,
                        productsCount: data.count,
                        activePage: 1,
                        pagesCount: pagesCount,
                        loaded: true,
                        baseUrl: `/api/v1/shop/` + this.state.shopSlug + '/'
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

    // changeDeliveryType: function (deliveryType) {
    //     this.setState({
    //         deliveryType: deliveryType
    //     });
    // },

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
        var owner = this.state.owner;

        // if (this.state.activeCategories.length > 0) {
        //     filteredProducts = _.filter(filteredProducts, function (item) {
        //         return _.indexOf(this.state.activeCategories, item.category_title) != -1
        //     }.bind(this));
        // }
        // ;

        filteredProducts = this.state.products.map(function (item, index) {
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

        var productsCount = filteredProducts.length;

        return (
            <div>
                <div className="col-md-12 col-lg-3">
                    <ul>

                        <li>Все категории</li>
                        {categories}
                    </ul>
                </div>
                <div className="col-md-12 col-lg-9">
                    <SearchForm
                        orderBy={ this.state.orderBy }
                        onReOrder={ this.reOrder }
                        onSearch={ this.searchApts }
                        priceFrom={ this.state.priceFrom }
                        query={this.state.queryText}
                        priceTo={ this.state.priceTo }
                        onChangePriceFrom={ this.changePriceFrom }
                        onChangePriceTo={ this.changePriceTo }
                    />
                    {owner ?
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
                        : null}
                    <Loader loaded={this.state.loaded}>
                    {filteredProducts}
                    </Loader>
                    <div className="clearfix"></div>

                     {this.state.pagesCount > 1 ?
                        <Pagination
                          activePage={this.state.activePage}
                          itemsCountPerPage={21}
                          totalItemsCount={this.state.productsCount}
                          pageRangeDisplayed={5}
                          onChange={this.handlePageChange}
                        />
                    : ''}
                </div>
            </div>
        )
    }
});


ReactDOM.render(<MainInterface />, document.getElementById('root'));

$('.select-beast').selectize({});

