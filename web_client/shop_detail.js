import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/ShopDetailProducts';
import SearchForm from './components/ShopDetailSearchForm';
import CategoryList from './components/ShopDetailCategory';
import _ from 'lodash';
import Pagination from 'react-js-pagination';



var MainInterface = createClass({
    displayName: 'MainInterface',

    getInitialState: function () {
        return {
            orderBy: 'title',
            orderDir: 'asc',
            priceFrom: '',
            priceTo: '',
            queryText: '',
            deliveryType: 'all',
            productsCount: 0,
            pagesCount: 0,
            products: [],
            shops: [],
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
              url: `/api/v1/shop/` + this.state.shopSlug,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 21);
                    this.setState({
                        products: products,
                        next: data.next,
                        previous: data.previous,
                        productsCount: data.count,
                        activePage: 1,
                        pagesCount: pagesCount,
                        baseUrl: `/api/v1/shop/` + this.state.shopSlug + '/'
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })

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
        $.ajax({
            type: "GET",
              url: this.state.baseUrl + '?page=' + pageNumber,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    this.setState({
                        products: products,
                        activePage: pageNumber
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    },

    reOrder: function (orderBy, orderDir) {
        this.setState({
            orderBy: orderBy,
            orderDir: orderDir
        }); //setState
    }, //reOrder

    changeDeliveryType: function (deliveryType) {
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

        allProducts.forEach(function (item) {
            if (item.title.toLowerCase().indexOf(queryText) != -1) {
                if (item.delivery_type == deliveryType || deliveryType == 'all') {
                    filteredProducts.push(item);
                }
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


        var productsCount = filteredProducts.length

        filteredProducts = _.orderBy(filteredProducts, function (item) {
            if (orderBy == 'title') {
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
                        deliveryType={ this.state.deliveryType }
                        onChangeDeliveryType={ this.changeDeliveryType }
                        priceFrom={ this.state.priceFrom }
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
                    {filteredProducts}
                    <div className="clearfix"></div>
                    {/*<Pagination*/}
                        {/*goToPrevious={this.goToPreviousPage}*/}
                        {/*goToNext={this.goToNextPage}*/}
                        {/*goTo={this.goTo}*/}
                        {/*count={this.state.productsCount}*/}
                        {/*next={this.state.next}*/}
                        {/*previous={this.state.previous}*/}
                        {/*page={this.state.currentPage}*/}
                        {/*pagesCount={this.state.pagesCount}*/}
                        {/*baseUrl={this.state.baseUrl}*/}
                     {/*/>*/}

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

