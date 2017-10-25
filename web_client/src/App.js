import React, { Component } from 'react';
import urlmaker from './urlmaker';
import Product from './components/Product';
import SearchForm from './components/SearchFrom';
import CategoryList from "./components/CategoryList";
import ChildCategory from "./components/ChildCategory";
import Shop from './components/Shop';
import Pagination from 'react-js-pagination';
import $ from 'jquery';

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
        parentCategories: [],
        activeCategory: '',
        pageType: this.pageType(),
        loaded: false,
        places: [],
        markets: [],
        activePlace: '',
        productsByPage: 20,
        domain: window.location.href.split("/")[2].split(":")[0],
        categorySlug: window.location.href.split("/")[window.location.href.split("/").length - 2],
        shopSlug: this.pageType() === 'shop' ? window.location.href.split("/")[4] : null
    }
  }

  pageType = () => {
       if (window.location.href.split("/")[4] && window.location.href.split("/")[4] === 'parent') {
           return "parent"
       } else if(window.location.href.split("/").length === 5 && window.location.href.split("/")[3] === 'shops') {
            return "shops"
        } else if (window.location.href.split("/")[3] && window.location.href.split("/")[3] === 'shops') {
            return "shop"
        } else if (window.location.href.split("/").length === 6) {
            return "child"
        } else {
            return "global"
        }
  };

  getMatchPhrase = () => {
    if (this.state.pageType === 'global') {
        return {global_slug: this.state.categorySlug}
    } else if (this.state.pageType === 'parent') {
        return {parent_category_slug: this.state.categorySlug}
    } else if (this.state.pageType === 'shop') {
        return {shop_slug: this.state.shopSlug}
    } else {
        return {category_slug: this.state.categorySlug}
    }
  };

  componentDidMount = () => {
        const params = window.location.search.substr(1).split("&");
        params.forEach(function (i) {
            if (i.split("=")[0] === "q") {
                this.setState({
                    queryText: i.split("=")[1]
                })
            }
        }.bind(this));

        if (this.state.pageType === 'shops') {
            $.ajax({
                type: "GET",
                  url: `/api/v1/shop/`,
                  success: function (data) {
                        let shops = data.results.map(obj =>obj);
                        let pagesCount = Math.ceil(data.count / 24);
                        this.setState({
                            shops: shops,
                            pagesCount: pagesCount,
                            shopCount: data.count,
                        });
                  }.bind(this),
                  error: function (response, error) {
                      console.log(response);
                      console.log(error);
                  }
                });
                $.ajax({
                 type: "GET",
                  url: `/api/v1/place/`,
                  success: function (data) {
                        let places = data.map(obj =>obj);
                        this.setState({
                            places: places,
                            loaded: true
                        });
                  }.bind(this),
                  error: function (response, error) {
                      console.log(response);
                      console.log(error);
                  }
            })

        } else {
            const query = {
                query: {
                    match_phrase: this.getMatchPhrase()
                },
                size:  this.state.productsByPage,
                from: 0,
                sort: [
                    {created_at: "desc"},
                ]
              };

      $.ajax({
            type: "GET",
              url: `http://${this.state.domain}:8000/api/v1/my-list/`,
              success: function (data) {
                    let favorites = data.favorites.map(obj => obj.id);
                    let cartItems = data.cart_items.map(obj => obj.id);
                    let shops = data.shops.map(obj => obj.title);
                    this.setState({
                        favorites: favorites,
                        cartItems: cartItems,
                        shops: shops
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        });

      if (this.state.pageType === 'shop') {
          $.ajax({
            type: "GET",
              url: `/api/v1/shop/` + this.state.shopSlug + '/shop/for-react/',
              success: function (data) {
                    let owner = data[0].shop[0].is_owner;
                    let parentCategories = data[1].category.map(obj =>obj);
                    let categories = data[2].category.map(obj =>obj);
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
      }

          $.ajax({
                type: "POST",
                url: `http://${this.state.domain}:9200/_search/`,
                data: JSON.stringify(query),
                success: function (data) {
                        const products = data.hits.hits.map(obj => obj._source);
                        const pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                        this.setState({
                            products: products,
                            productsCount: data.hits.total,
                            activePage: 1,
                            pagesCount: pagesCount,
                            loaded: true
                        });
                  }.bind(this),
                  error: function (response, error) {
                      console.log(response);
                      console.log(error);
                  }
            })
        }


  };

  handlePageChange = (pageNumber) => {
        this.setState({
           loaded: false
        });

        if (this.state.pageType === 'shops') {
             $.ajax({
                    type: "GET",
                      url: '/api/v1/shop/?page=' + pageNumber + '&q=' + this.state.queryText + '&place=' + this.state.activePlace,
                      success: function (data) {
                            let shops = data.results.map(obj => obj);
                            this.setState({
                                shops: shops,
                                activePage: pageNumber,
                                loaded: true,
                            });
                      }.bind(this),
                      error: function (response, error) {
                          console.log(response);
                          console.log(error);
                      }
                })
        } else {
            let query = urlmaker(this.state.productsCount, this.state.productsByPage, pageNumber,
                            this.state.activePage, this.state.orderBy, this.state.priceFrom,
                            this.state.priceTo, this.state.queryText, this.state.categorySlug,
                            this.getMatchPhrase(), this.state.shopSlug, this.state.activeCategory,
                            this.state.parent ? this.state.parent : null);
              $.ajax({
                    type: "POST",
                    url: `http://${this.state.domain}:9200/_search/`,
                    data: JSON.stringify(query),
                    success: function (data) {
                           const products = data.hits.hits.map(obj => obj._source);
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
        }


  };

  handleChangePlace = (e) => {
        if (isNaN(e.target.value)) {
            var activePlace = '';
        } else {
            var activePlace = parseInt(e.target.value);
        }
        this.setState({
            loaded: false,
        });
        $.ajax({
            type: "GET",
              url: '/api/v1/shop/?page=' + this.state.activePage + '&q=' + this.state.queryText + '&place=' + activePlace,
              success: function (data) {
                    let shops = data.results.map(obj => obj);
                    let pagesCount = Math.ceil(data.count / 24);
                    this.setState({
                        shops: shops,
                        loaded: true,
                        pagesCount: pagesCount,
                        shopCount: data.count,
                        activePage: 1,
                        activePlace: activePlace
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
  };

  reOrder = (orderBy) => {
      this.setState({
           loaded: false
        });

        let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            this.state.activePage, orderBy, this.state.priceFrom,
                            this.state.priceTo, this.state.queryText, this.state.categorySlug,
                            this.getMatchPhrase(), this.state.shopSlug, this.state.activeCategory,
                            this.state.parent ? this.state.parent : null);

      $.ajax({
            type: "POST",
            url: `http://${this.state.domain}:9200/_search/`,
            data: JSON.stringify(query),
            success: function (data) {
                   const products = data.hits.hits.map(obj => obj._source);
                    this.setState({
                        products: products,
                        orderBy: orderBy,
                        loaded: true,
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
  };

  searchApts = (q) => {
      if (this.state.pageType === 'shops') {
          let query = q;
        this.setState({
            loaded: false,
        });
        $.ajax({
            type: "GET",
              url: '/api/v1/shop/?page=' + this.state.activePage + '&q=' + query + '&place=' + this.state.activePlace,
              success: function (data) {
                    let shops = data.results.map(obj => obj);
                    let pagesCount = Math.ceil(data.count / 24);
                    this.setState({
                        shops: shops,
                        loaded: true,
                        pagesCount: pagesCount,
                        shopCount: data.count,
                        queryText: query,
                        activePage: 1
                    });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
      } else {
              this.setState({
               loaded: false
            });

            let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                                this.state.activePage, this.state.orderBy, this.state.priceFrom,
                                this.state.priceTo, q, this.state.categorySlug, this.getMatchPhrase(),
                                this.state.shopSlug, this.state.activeCategory,
                                this.state.parent ? this.state.parent : null);

          $.ajax({
                    type: "POST",
                    url: `http://${this.state.domain}:9200/_search/`,
                    data: JSON.stringify(query),
                    success: function (data) {
                           let products = data.hits.hits.map(obj => obj._source);
                            let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
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
      }

  };

  changePriceFrom = (price) => {
      this.setState({
           loaded: false
        });

        let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            this.state.activePage, this.state.orderBy, price,
                            this.state.priceTo, this.state.queryText, this.state.categorySlug,
                            this.getMatchPhrase(), this.state.shopSlug, this.state.activeCategory,
                            this.state.parent ? this.state.parent : null);

      $.ajax({
            type: "POST",
            url: `http://${this.state.domain}:9200/_search/`,
            data: JSON.stringify(query),
            success: function (data) {
                   let products = data.hits.hits.map(obj => obj._source);
                    let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                    this.setState({
                        products: products,
                        loaded: true,
                        priceFrom: parseInt(price, 10),
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
  };

  changePriceTo = (price) => {
      this.setState({
           loaded: false
        });

        let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            this.state.activePage, this.state.orderBy, this.state.priceFrom,
                            price, this.state.queryText, this.state.categorySlug, this.getMatchPhrase(),
                            this.state.shopSlug, this.state.activeCategory, this.state.parent ? this.state.parent : null);

        $.ajax({
            type: "POST",
            url: `http://${this.state.domain}:9200/_search/`,
            data: JSON.stringify(query),
            success: function (data) {
                   let products = data.hits.hits.map(obj => obj._source);
                let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                this.setState({
                    products: products,
                    loaded: true,
                    priceTo: parseInt(price, 10),
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
  };

    handleCategorySort = (id) => {
        this.setState({
            loaded: false
        });
         let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            1, this.state.orderBy, this.state.priceFrom,
                            this.state.priceTo, '', this.state.categorySlug, this.getMatchPhrase(),
                            this.state.shopSlug, id, true);

       $.ajax({
            type: "POST",
            url: `http://${this.state.domain}:9200/_search/`,
            data: JSON.stringify(query),
            success: function (data) {
                  let products = data.hits.hits.map(obj => obj._source);
                let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
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
    };

    handleChildCategorySort = (id) => {
        this.setState({
            loaded: false
        });
         let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            1, this.state.orderBy, this.state.priceFrom,
                            this.state.priceTo, null, this.state.categorySlug, this.getMatchPhrase(),
                            this.state.shopSlug, id, false);

         $.ajax({
            type: "POST",
            url: `http://${this.state.domain}:9200/_search/`,
            data: JSON.stringify(query),
            success: function (data) {
                  let products = data.hits.hits.map(obj => obj._source);
                let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
                this.setState({
                    products: products,
                    loaded: true,
                    pagesCount: pagesCount,
                    productsCount: data.hits.total,
                    activePage: 1,
                    activeCategory: id,
                    parent: false,
                    fromPage: 21
                });
              }.bind(this),
              error: function (response, error) {
                  console.log(response);
                  console.log(error);
              }
        })
    };

    deleteActiveCategory = (e) => {
      e.preventDefault();
      this.setState({
          loaded: false
      });
      let query = urlmaker(this.state.productsCount, this.state.productsByPage, 1,
                            1, this.state.orderBy, this.state.priceFrom,
                            this.state.priceTo, null, this.state.categorySlug, this.getMatchPhrase(),
                            this.state.shopSlug, '', false);

      $.ajax({
            type: "POST",
            url: `http://${this.state.domain}:9200/_search/`,
            data: JSON.stringify(query),
            success: function (data) {
                  let products = data.hits.hits.map(obj => obj._source);
                let pagesCount = Math.ceil(data.hits.total / this.state.productsByPage);
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

    };

  render() {
        if (this.state.pageType === 'shops'){
            let filteredShops = [];
            let subscribe = this.subscribe;

        filteredShops = this.state.shops.map(function (item) {
            return (
                <Shop
                    key={item.id}
                    shop={item}
                    subscribe={subscribe}
                />
            )
        });

        return (
        <section className="shop-list uk-margin-large-top">
        <div className="uk-container">
            <h3 className="uk-margin-medium-bottom"><a href="">Магазины</a></h3>

                <form action="" className="uk-grid uk-margin-medium-bottom uk-grid-small uk-flex-right uk-child-width-1-4@s uk-child-width-1-1" data-uk-grid>
                    <div className="">
                        <select className="uk-select" onChange={this.handleChangePlace}>
                        <option>Выбрать ТЦ</option>
                          {this.state.places.map(function (item, index) {
                            return (
                              <option
                                key={index}
                                value={item.id}>{item.title} {item.ttype}</option>
                            );
                          })}
                        </select>
                    </div>

                    <div className="">
                        <div class="uk-inline uk-width-1-1">
                            <button type="submit" className="uk-form-icon uk-form-icon-flip" data-uk-icon="icon: search"></button>
                            <input className="uk-input uk-width-1-1" type="search" placeholder="Поиск магазина..." onChange={this.searchApts} />
                        </div>
                    </div>
                </form>


                    <div className="uk-child-width-1-1 uk-child-width-1-2@s uk-child-width-1-3@m uk-grid-small uk-child-width-1-4@l " data-uk-grid>
                        {filteredShops}
                    </div>


                {this.state.pagesCount > 1 ?
                        <Pagination
                          activePage={this.state.activePage}
                          itemsCountPerPage={24}
                          totalItemsCount={this.state.shopCount}
                          pageRangeDisplayed={5}
                          onChange={this.handlePageChange}
                        />
                    : ''}

            </div>
        </section>
        )
        } else {
            let filteredProducts = [];
        let productDelete = this.productDelete;
        let categories = [];
        let descendants = [];

        filteredProducts = this.state.products.map(function (item, index) {
            return (
                <Product key={ item.pk }
                         onProductDelete={productDelete}
                         favorites={this.state.favorites}
                         cartItems={this.state.cartItems}
                         shops={this.state.shops}
                         product={ item }/>
            ) //return
        }.bind(this));

        if (this.state.pageType === 'shop') {
           categories = this.state.parentCategories.map(function (parent) {
            descendants = this.state.categories.filter(function(item){
                return item.parent_id === parent.id
            }).map(function (item) {
                    return (
                        <ChildCategory
                            key={item.id}
                            category={item}
                            // onChangeCategory={this.changeCategory}
                            activeCategory={this.state.activeCategory}
                            categorySort={this.handleChildCategorySort}
                        />
                    )
            }.bind(this));
            return (
                <CategoryList
                    key={parent.id}
                    category={parent}
                    descendants={descendants}
                    // onChangeCategory={this.changeCategory}
                    activeCategory={this.state.activeCategory}
                    categorySort={this.handleCategorySort}
                />
            )
        }.bind(this));
        }


        return (
            <div className="uk-container">
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

                    {this.state.pageType === "shop" ? (
                        <div className="uk-grid uk-grid-small">
                            <div className="uk-width-1-4@m">
                                <ul data-uk-accordion="collapsible: true; duration: 600;">
                                    <li className={this.state.activeCategory === '' && 'uk-open'}>
                                        <a className="uk-accordion-title uk-display-block uk-text-left" onClick={this.deleteActiveCategory}>
                                         Все категории
                                        </a>
                                    </li>
                                    {categories}
                                </ul>
                            </div>
                            <div className="uk-width-expand@m">
                                <div className="uk-child-width-1-1 uk-child-width-1-2@s uk-child-width-1-2@m  uk-child-width-1-3@l uk-grid-small" data-uk-grid>

                                    {this.state.isOwner && (
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
                                    )}



                                    {filteredProducts}


                                </div>
                            </div>

                        </div>
                    ): (
                        <div className="uk-child-width-1-1 uk-child-width-1-2@s uk-child-width-1-3@m  uk-child-width-1-4@l uk-grid-small" data-uk-grid>
                            {filteredProducts}
                        </div>
                    )}




                {this.state.pagesCount > 1 ?
                    <Pagination
                      activePage={this.state.activePage}
                      itemsCountPerPage={this.state.productsByPage}
                      totalItemsCount={this.state.productsCount}
                      pageRangeDisplayed={5}
                      onChange={this.handlePageChange}
                    />
                : ''}
            </div>
        )
        }

  }
}

export default App;
