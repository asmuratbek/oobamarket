import React from "react";
import ReactDOM from "react-dom";
import createClass from "create-react-class";
import Product from "./components/ShopDetailProducts";
import SearchForm from "./components/SearchForm";
import CategoryList from "./components/ShopDetailCategory";
import ChildCategory from "./components/ChildCategory";
import _ from "lodash";
import Pagination from "react-js-pagination";
import Loader from "react-loader";


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
            fromPage: 21,
            pagesCount: 0,
            productsByPage: 21,
            products: [],
            shops: [],
            favorites: [],
            cartItems: [],
            loaded: false,
            parentCategories: [],
            categories: [],
            activeCategory: '',
            owner: false,
            domain: location.href.split("/")[2].split(":")[0],
            shopSlug: location.href.split("/")[4] ? location.href.split("/")[4] : location.href.split(".")[0].split("http://")[1]
        }
    },

    componentWillMount() {
        var params = location.search.substr(1).split("&")
        params.forEach(function (i) {
            if (i.split("=")[0] == "q") {q
                this.setState({
                    queryText: i.split("=")[1]
                })
            }
        }.bind(this));

        $.ajax({
            type: "GET",
              url: `/api/v1/shop/` + this.state.shopSlug + '/shop/for-react/',
              success: function (data) {
                   var owner = data[0].shop[0].is_owner;
                    var parentCategories = data[1].category.map(obj =>obj);
                    var categories = data[2].category.map(obj =>obj);
                    this.setState({
                        owner: owner,
                        parentCategories:parentCategories,
                        categories: categories

                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })

        var query = {
                'query': {
                    'match_phrase': {
                        'shop_slug': this.state.shopSlug
                    }
                },
                "size":  this.state.productsByPage,
                "from": 0,
                "sort": [
                    {"created_at": "desc"},
                ]
              };

        $.ajax({
            type: "POST",
              url: `http://${this.state.domain}:9200/_search/`,
              data: JSON.stringify(query),
              contentType: 'application/json',
              dataType : 'json',
              success: function (data) {
                    var products = data.hits.hits.map(obj => obj._source);
                    var pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                    this.setState({
                        products: products,
                        productsCount: data.hits.total,
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

         $.ajax({
            type: "GET",
              url: `http://${this.state.domain}:8000/api/v1/my-list/`,
              success: function (data) {
                    var favorites = data.favorites.map(obj => obj.id);
                    var cartItems = data.cart_items.map(obj => obj.id);
                    this.setState({
                        favorites: favorites,
                        cartItems: cartItems
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
    // productDelete: function (item) {
    //     var allProducts = this.state.products;
    //     var deleted = _.remove(allProducts, function (n) {
    //         return n.pk == item;
    //     });
    //     var newProducts = _.without(allProducts, deleted);
    //     this.setState({
    //         products: newProducts
    //     }); //setState
    // },
    handlePageChange: function(pageNumber) {
        var from = this.state.productsCount > this.state.productsByPage * pageNumber ? (
            this.state.productsByPage * pageNumber
        ) : (
            this.state.activePage * this.state.productsByPage
        );
        console.log(this.state.fromPage);
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
        if (this.state.queryText && this.state.activeCategory) {
          var q = [
              { "match": { "text":  this.state.queryText }},
              { "match_phrase": { "shop_slug":  this.state.shopSlug }},
              { "match_phrase": { "category_id": this.state.activeCategory }}

          ]
        } else if (this.state.queryText) {
            var q = [
                { "match": { "text":  this.state.queryText }},
                { "match_phrase": { "shop_slug":  this.state.shopSlug }},
            ]
        } else if (this.state.activeCategory && this.state.parent) {
           var q = [
                { "match_phrase": { "parent_category_id": this.state.activeCategory }},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else if (this.state.activeCategory && !this.state.parent ) {
           var q = [
                { "match_phrase": { "category_id": this.state.activeCategory }},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else {
            var q = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }}
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
                "from": pageNumber == 1 ? 0 : this.state.fromPage,
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
                    this.setState({
                        products: products,
                        activePage: pageNumber,
                        fromPage: from,
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
        if (this.state.queryText && this.state.activeCategory) {
          var q = [
              { "match": { "text":  this.state.queryText }},
              { "match_phrase": { "shop_slug":  this.state.shopSlug }},
              { "match": { "category_id": this.state.activeCategory }}

          ]
        } else if (this.state.queryText) {
            var q = [
                {"match": {"text": this.state.queryText}},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else if (this.state.activeCategory) {
           var q = [
                { "match": { "category_id": this.state.activeCategory }},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else {
            var q = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }}
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

    // changeDeliveryType: function (deliveryType) {
    //     this.setState({
    //         deliveryType: deliveryType
    //     });
    // },

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
        if (q && this.state.activeCategory) {
          var queryset = [
              { "match": { "text":  q }},
              { "match_phrase": { "shop_slug":  this.state.shopSlug }},
              { "match": { "category_id": this.state.activeCategory }}

          ]
        } else if (q) {
            var queryset = [
                {"match": {"text": q}},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else if (this.state.activeCategory) {
           var queryset = [
                { "match": { "category_id": this.state.activeCategory }},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else {
            var queryset = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }}
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
                    var pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
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
        if (this.state.queryText && this.state.activeCategory) {
          var q = [
              { "match": { "text":  this.state.queryText }},
              { "match_phrase": { "shop_slug":  this.state.shopSlug }},
              { "match": { "category_id": this.state.activeCategory }}

          ]
        } else if (this.state.queryText) {
            var q = [
                {"match": {"text": this.state.queryText}},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else if (this.state.activeCategory) {
           var q = [
                { "match": { "category_id": this.state.activeCategory }},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else {
            var q = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }}
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
        if (this.state.queryText && this.state.activeCategory) {
          var q = [
              { "match": { "text":  this.state.queryText }},
              { "match_phrase": { "shop_slug":  this.state.shopSlug }},
              { "match": { "category_id": this.state.activeCategory }}

          ]
        } else if (this.state.queryText) {
            var q = [
                {"match": {"text": this.state.queryText}},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else if (this.state.activeCategory) {
           var q = [
                { "match": { "category_id": this.state.activeCategory }},
                {"match_phrase": {"shop_slug": this.state.shopSlug}},
            ]
        } else {
            var q = [
                { "match": { "shop_slug":  this.state.shopSlug }}
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

    changeCategory(title) {
        var activeCategory = this.state.activeCategory;
        if (activeCategory.indexOf(title) != -1) {
            activeCategory = _.without(activeCategory, title);
        }
        else {
            activeCategory.push(title);
        }
        this.setState({
            activeCategory: activeCategory
        })
    },

    handleCategorySort(id){
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

        if (this.state.priceTo && this.state.priceFrom) {
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
        if (this.state.queryText && id) {
            var q = [
                { "match": { "text":  this.state.queryText }},
                { "match_phrase": { "shop_slug":  this.state.shopSlug }},
                { "match": { "parent_category_id": id }}
            ]
        } else if (id) {
            var q = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }},
                { "match": { "parent_category_id": id }}
            ]
        } else {
            var q = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }}
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
                        pagesCount: pagesCount,
                        productsCount: data.hits.total,
                        activePage: 1,
                        activeCategory: id,
                        parent: true,
                        fromPage: 21
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    },

    handleChildCategorySort(id){
        console.log(id);
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

        if (this.state.priceTo && this.state.priceFrom) {
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
        if (this.state.queryText && id) {
            var q = [
                { "match": { "text":  this.state.queryText }},
                { "match_phrase": { "shop_slug":  this.state.shopSlug }},
                { "match": { "category_id": id }}
            ]
        } else if (id) {
            var q = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }},
                { "match": { "category_id": id }}
            ]
        } else {
            var q = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }}
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
                        pagesCount: pagesCount,
                        productsCount: data.hits.total,
                        activePage: 1,
                        activeCategory: id,
                        parent: false,
                        fromPage: 21,
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    },

    deleteActiveCategory(e) {
      e.preventDefault();
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

        if (this.state.priceTo && this.state.priceFrom) {
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
                { "match_phrase": { "shop_slug":  this.state.shopSlug }},
            ]
        } else {
            var q = [
                { "match_phrase": { "shop_slug":  this.state.shopSlug }}
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
                        activeCategory: '',
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
        var categories = [];
        var allProducts = this.state.products;
        var orderBy = this.state.orderBy;
        var queryText = this.state.queryText;
        var orderDir = this.state.orderDir;
        var deliveryType = this.state.deliveryType;
        var changeCategory = this.changeCategory;
        var activeCategory = this.state.activeCategory;
        // var productDelete = this.productDelete;
        var owner = this.state.owner;
        var handleCategorySort = this.handleCategorySort;
        var handleChildCategorySort = this.handleChildCategorySort;
        var descendants = [];

        filteredProducts = this.state.products.map(function (item, index) {
            return (
                <Product key={ index }
                         // onProductDelete={productDelete}
                        favorites={this.state.favorites}
                         cartItems={this.state.cartItems}
                         product={ item }
                         owner={ this.state.owner }
                />
            ) //return
        }.bind(this));


        categories = this.state.parentCategories.map(function (parent, parentIndex) {
            descendants = this.state.categories.map(function (item, index) {
                if (item.parent_id == parent.id) {
                    return (
                        <ChildCategory
                            key={index}
                            category={item}
                            onChangeCategory={changeCategory}
                            activeCategory={activeCategory}
                            categorySort={handleChildCategorySort}
                        />
                    )
                }
            }.bind(this));
            return (
                <CategoryList
                    key={parentIndex}
                    category={parent}
                    descendants={descendants}
                    onChangeCategory={changeCategory}
                    activeCategory={activeCategory}
                    categorySort={handleCategorySort}
                />
            )
        }.bind(this));

        return (
            <div>
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
                    <div className="uk-grid uk-grid-small">
                    <div className="uk-width-1-4@m">
                        <ul data-uk-accordion="collapsible: false; duration: 600;">
                            <li>
                                <a className="uk-accordion-title uk-display-block uk-text-left">
                                 Очень длинный текст категории
                                </a>
                                <div className="uk-accordion-content">
                                    <a href="" className="uk-display-block ">asdasd</a>
                                </div>

                            </li>
                            <li>
                                <a className="uk-accordion-title uk-display-block uk-text-left">
                                    сыылка
                                </a>
                                <div className="uk-accordion-content">
                                    <a href="" className="uk-display-block">asdasd</a>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <div className="uk-width-expand@m">
                        <div className="uk-child-width-1-1 uk-child-width-1-2@s uk-child-width-1-2@m  uk-child-width-1-3@l uk-grid-small" data-uk-grid>

                            <div className="uk-grid-match add-product-item">
                                <div className="shadow uk-text-center">
                                    <div className="uk-inline-clip uk-transition-toggle">
                                        <div className="border">
                                            <a href="" className="uk-position-cover">{}</a>
                                            <div className="uk-cover-container">
                                                <div className="cover">
                                                    <span className="uk-display-block uk-margin-small-bottom" data-uk-icon="ratio: 3; icon:  plus-circle">{}</span>
                                                    Добавить новый товар
                                                </div>

                                                <canvas width="400" height="500">{}</canvas>
                                                <img data-uk-cover src="img/white.jpg" alt=""/>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="uk-padding-small uk-margin-remove uk-padding-remove footer">
                                       <a href="">Добавить акцию</a>
                                    </div>
                                </div>
                            </div>


                            {filteredProducts}


                        </div>
                    </div>

                </div>
            </div>
        )
    }
});


ReactDOM.render(<MainInterface />, document.getElementById('root'));

$('.select-beast').selectize({});

