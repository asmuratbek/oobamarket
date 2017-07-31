import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/ShopDetailProducts';
import SearchForm from './components/ShopDetailSearchForm';
import CategoryList from './components/ShopDetailCategory';
import _ from 'lodash';


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
            products: [],
            shop: [],
            categories: [],
            activeCategories: [],
            shopSlug: location.href.split("/")[4]
        }
    },

    componentWillMount() {

        // axios.get(`/api/shops/` + this.state.shopSlug)
        //     .then(res => {
        //         var owner = res.data[0].shop[0].is_owner;
        //         var categories = res.data[2].category.map(obj => obj);
        //         var products = res.data[1].product.map(obj => obj);
        //         this.setState({
        //             owner: owner,
        //             categories: categories,
        //             products: products
        //         });
        //     });

        $.ajax({
            type: "GET",
              url: `/api/shops/` + this.state.shopSlug,
              success: function (data) {
                    var owner = data[0].shop[0].is_owner;
                    var categories = data[2].category.map(obj =>obj);
                    var products = data[1].product.map(obj => obj);
                    this.setState({
                        owner: owner,
                        categories:categories,
                        products: products,
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
                    index={index}
                    onChangeCategory={changeCategory}
                    activeCategories={activeCategories}
                />
            )
        });


        var productsCount = filteredProducts.length;

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
                    <nav className="pagination">
                        <ul>
                            <li>
                                <a href="#" aria-label="Previous">
                                    <span aria-hidden="true">&laquo;</span>
                                </a>
                            </li>
                            <li><a href="#">1</a></li>
                            <li><a href="#">2</a></li>
                            <li><a href="#">3</a></li>
                            <li><a href="#">4</a></li>
                            <li><a href="#">5</a></li>
                            <li>
                                <a href="#" aria-label="Next">
                                    <span aria-hidden="true">&raquo;</span>
                                </a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        )
    }
});

ReactDOM.render(<MainInterface />, document.getElementById('root'));
