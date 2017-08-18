import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Pagination from 'react-js-pagination';
import Loader from 'react-loader';
import ShopDetail from './components/ShopDetail';


var MainInterface = createClass({
    displayName: 'MainInterface',

    getInitialState() {
        return {
            queryText: '',
            shops: [],
            places: [],
            loaded: false,
            markets: [],
            activePlace: '',
            activePage: 1
        }
    },

    componentWillMount() {
        $.ajax({
            type: "GET",
              url: `/api/v1/shop/`,
              success: function (data) {
                    var shops = data.results.map(obj =>obj);
                    var pagesCount = Math.ceil(data.count / 8);
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
                    var places = data.map(obj =>obj);
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
    },

    handlePageChange: function(pageNumber) {
        this.setState({
           loaded: false
        });
        $.ajax({
            type: "GET",
              url: '/api/v1/shop/?page=' + pageNumber + '&q=' + this.state.queryText + '&place=' + this.state.activePlace,
              success: function (data) {
                    var shops = data.results.map(obj => obj);
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
    },

    handleChangePlace(e) {
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
                    var shops = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 8);
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
    },

    searchApts(e) {
        var query = e.target.value;
        this.setState({
            loaded: false,
        });
        $.ajax({
            type: "GET",
              url: '/api/v1/shop/?page=' + this.state.activePage + '&q=' + query + '&place=' + this.state.activePlace,
              success: function (data) {
                    var shops = data.results.map(obj => obj);
                    var pagesCount = Math.ceil(data.count / 8);
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
    },


    render: function () {
        var filteredShops = [];
        var subscribe = this.subscribe;

        filteredShops = this.state.shops.map(function (item, index) {
            return (
                <ShopDetail
                    key={index}
                    shop={item}
                    subscribe={subscribe}
                />
            )
        });

        return (
        <div className="container">
            <div className="row">
                <h1 className="pull-left">Магазины</h1>
                <form action="" className="pull-right col-md-6">
                    <select className="demo-default col-md-5" onChange={this.handleChangePlace}>
                        <option>Выбрать ТЦ</option>
                          {this.state.places.map(function (item, index) {
                            return (
                              <option
                                key={index}
                                value={item.id}>{item.ttype} {item.title}</option>
                            );
                          })}
                    </select>
                    <div className="form-search col-md-7">
                        <input className="form-control" type="search" placeholder="Поиск магазина..." onChange={this.searchApts} />
                        <button type="submit">
                            <span className="glyphicon glyphicon-search"></span>
                        </button>
                    </div>
                </form>
                <div className="clearfix"></div>

                <div className="bg-white">
                    <Loader loaded={this.state.loaded}>
                    {filteredShops}
                    </Loader>
                </div>
                {this.state.pagesCount > 1 ?
                        <Pagination
                          activePage={this.state.activePage}
                          itemsCountPerPage={8}
                          totalItemsCount={this.state.shopCount}
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
