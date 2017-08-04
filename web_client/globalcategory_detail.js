import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/Product';
import SearchForm from './components/SearchForm';
import CategoryList from './components/CategoryList';
import _ from 'lodash';
import Pagination from './components/Pagination';



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
        // axios.get(`/product/api/`)
        //     .then(res => {
        //         const products = res.data.map(obj => obj);
        //         this.setState({
        //             products: products,
        //             categories: _.uniqBy(products.map(obj => obj.get_category_title), obj => obj)
        //         });
        //     });
        // axios.get(`/api/globalcategory/` + this.state.categorySlug)
        //     .then(res => {
        //         var products = res.data[0].product.map(obj => obj);
        //         this.setState({
        //             products: products,
        //         });
        //     });

        $.ajax({
            type: "GET",
              url: `/api/globalcategory/` + this.state.categorySlug,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 20);
                    this.setState({
                        products: products,
                        next: data.next,
                        previous: data.previous,
                        productsCount: data.count,
                        currentPage: "1",
                        pagesCount: pagesCount,
                        baseUrl: `/api/globalcategory/` + this.state.categorySlug + '/',
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

    goToNextPage: function () {
      $.ajax({
            type: "GET",
              url: this.state.next,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    this.setState({
                        products: products,
                        next: data.next,
                        previous: data.previous,
                        productsCount: data.count,
                        currentPage: this.state.next.split('?')[1].split('=')[1]
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    },

    goToPreviousPage: function() {
        $.ajax({
            type: "GET",
              url: this.state.previous,
              success: function (data) {
                    var products = data.results.map(obj => obj);
                    this.setState({
                        products: products,
                        next: data.next,
                        previous: data.previous,
                        productsCount: data.count,
                        currentPage: this.state.previous.split('?').length > 1 ? this.state.previous.split('?')[1].split('=')[1] : "1"
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

                <ul className="category-tab">
                    {categories}
                </ul>
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
                <div className="item-filter">
                    {filteredProducts}
                    <div className="clearfix"></div>
                </div>

                {/*<div className="catalog-filter">*/}
                    {/*<h4>Параметры</h4>*/}
                    {/*<div className="filter-clone">*/}
                        {/*<a className="btn-toggle-setting">*/}
                            {/*Производитель*/}
                        {/*</a>*/}
                        {/*<div className="toggle-setting" id="toggle-setting-1">*/}
                            {/*<div className="form-group checkbox">*/}

                                {/*<div className="cover">*/}
                                    {/*<div className="form-custom-checkbox">*/}
                                        {/*<label className="name_setting" htmlFor="slug1">Название настроек</label>*/}
                                        {/*<input type="checkbox" value="" name="" id="slug1"></input>*/}
                                        {/*<div className="indicator"></div>*/}
                                    {/*</div>*/}
                                {/*</div>*/}
                                {/*<div className="cover">*/}
                                    {/*<div className="form-custom-checkbox">*/}
                                        {/*<label className="name_setting" htmlFor="slug2">Название настроек</label>*/}
                                        {/*<input type="checkbox" value="" name="" id="slug2"></input>*/}
                                        {/*<div className="indicator"></div>*/}
                                    {/*</div>*/}
                                {/*</div>*/}
                                {/*<div className="cover">*/}
                                    {/*<div className="form-custom-checkbox">*/}
                                        {/*<label className="name_setting" htmlFor="slug3">Название настроек</label>*/}
                                        {/*<input type="checkbox" value="" name="" id="slug3"></input>*/}
                                        {/*<div className="indicator"></div>*/}
                                    {/*</div>*/}
                                {/*</div>*/}
                            {/*</div>*/}
                        {/*</div>*/}
                    {/*</div>*/}

                    {/*<div className="filter-clone" id="toggle-setting-2">*/}
                        {/*<a className="btn-toggle-setting">*/}
                            {/*Производитель*/}
                        {/*</a>*/}
                        {/*<div className="toggle-setting">*/}
                            {/*<div className="form-group checkbox">*/}

                                {/*<div className="cover">*/}
                                    {/*<div className="form-custom-checkbox">*/}
                                        {/*<label className="name_setting" htmlFor="slug1">Название настроек</label>*/}
                                        {/*<input type="checkbox" value="" name="" id="slug1"></input>*/}
                                        {/*<div className="indicator"></div>*/}
                                    {/*</div>*/}
                                {/*</div>*/}
                                {/*<div className="cover">*/}
                                    {/*<div className="form-custom-checkbox">*/}
                                        {/*<label className="name_setting" htmlFor="slug2">Название настроек</label>*/}
                                        {/*<input type="checkbox" value="" name="" id="slug2"></input>*/}
                                        {/*<div className="indicator"></div>*/}
                                    {/*</div>*/}
                                {/*</div>*/}
                                {/*<div className="cover">*/}
                                    {/*<div className="form-custom-checkbox">*/}
                                        {/*<label className="name_setting" htmlFor="slug3">Название настроек</label>*/}
                                        {/*<input type="checkbox" value="" name="" id="slug3"></input>*/}
                                        {/*<div className="indicator"></div>*/}
                                    {/*</div>*/}
                                {/*</div>*/}
                            {/*</div>*/}
                        {/*</div>*/}
                    {/*</div>*/}


                    {/*<div className="filter-clone">*/}
                        {/*<div className="form-group">*/}
                            {/*<select className="select-beast " placeholder="Название настроек">*/}
                                {/*<option value="">Название настроек</option>*/}
                                {/*<option value="4">Thomas Edison</option>*/}
                                {/*<option value="1">Nikola</option>*/}
                                {/*<option value="3">Nikola Tesla</option>*/}
                                {/*<option value="5">Arnold Schwarzenegger</option>*/}
                            {/*</select>*/}
                        {/*</div>*/}
                    {/*</div>*/}

                    {/*<div className="filter-clone">*/}
                        {/*<div className="form-group">*/}
                            {/*<select className="select-beast " placeholder="Название настроек">*/}
                                {/*<option value="">Название настроек</option>*/}
                                {/*<option value="4">Thomas Edison</option>*/}
                                {/*<option value="1">Nikola</option>*/}
                                {/*<option value="3">Nikola Tesla</option>*/}
                                {/*<option value="5">Arnold Schwarzenegger</option>*/}
                            {/*</select>*/}
                        {/*</div>*/}
                    {/*</div>*/}


                {/*</div>*/}

                <Pagination
                    goToPrevious={this.goToPreviousPage}
                    goToNext={this.goToNextPage}
                    count={this.state.productsCount}
                    next={this.state.next}
                    previous={this.state.previous}
                    page={this.state.currentPage}
                    pagesCount={this.state.pagesCount}
                    baseUrl={this.state.baseUrl}
                />

            </div>
        )
    }
});


ReactDOM.render(<MainInterface />, document.getElementById('root'));

$('.select-beast').selectize({});

