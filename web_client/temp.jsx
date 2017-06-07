var React = require('react');
var ReactDOM = require('react-dom');
var createClass = require('create-react-class');
var axios = require('axios');

var Products = createClass ({
    displayName: 'Products',

    getInitialState: function () {
      return {
          products: []
      }
    },

    componentDidMount() {
    axios.get(`http://localhost:8000/product/api/?limit=10`)
      .then(res => {
        const products = res.data.results.map(obj => obj);
        this.setState({ products });
      });
    },

    deliveryColor: function(product) {
        if (product.delivery_type == 'paid') {
            return (
                <span className="truck pull-right yellow" data-toggle="tooltip" title=""
                          data-placement="top" data-original-title={product.delivery_type_display}><i className="fa fa-truck" aria-hidden="true"></i></span>
            )
        }
        else if (product.delivery_type == 'free') {
            return (
                <span className="truck pull-right green" data-toggle="tooltip" title=""
                          data-placement="top" data-original-title={product.delivery_type_display}><i className="fa fa-truck" aria-hidden="true"></i></span>
            )
        }
        else {
            return (
                <span className="truck pull-right" data-toggle="tooltip" title=""
                          data-placement="top" data-original-title={product.delivery_type_display}><i className="fa fa-truck" aria-hidden="true"></i></span>
            )
        }
    },

    addOrRemoveFromCart : function (product) {

        $.ajax({
            type: "GET",
            url: "/cart/",
            data:
                {
                    "item":  product.id
                },
            success: function (data) {
                this.showFlashMessage(data.flash_message)

            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        });
    },

    inCart : function (product) {
      return (
          <a className="add-basket in-the-basket" data-product-id={product.id} onClick={() => this.addOrRemoveFromCart(product)}>
                        <span className="glyphicon glyphicon-shopping-cart"></span>
                        В корзине
                    </a>
      )
    },

    notInCart : function (product) {
      return (
          <a className="add-basket" data-product-id={product.id} onClick={() => this.addOrRemoveFromCart(product)}>
                        <span className="glyphicon glyphicon-shopping-cart"></span>
                        Добавить в корзину
                    </a>
      )
    },

    isInCart : function (product) {
        if (product.is_in_cart) {
            return (
                this.inCart(product)
            )
        } else {
            return (
                this.notInCart(product)
            )
        }
    },

  render() {

    return (
        <div className="container">
          {this.state.products.map(product =>

                <div className="col-md-3 col-sm-6" key={product.id}>
            <div className="cover">
                <a className="url-item" href={product.detail_view}></a>
                <div className="top-line">

                    <h2>
                        <a href={product.detail_view}>
                        {product.shop_title}
                        </a>
                    </h2>
                    {product.is_owner ?
                        <div>
                            <a className="edited glyphicon glyphicon-cog" href={`/products/${product.slug}/update_product/`} data-toggle="tooltip" title="" data-placement="bottom" data-original-title="Редактировать"></a>
                            <a className="eye glyphicon glyphicon-eye-open" data-toggle="tooltip" title="" data-placement="bottom" data-original-title="Скрыть" data-status="false"></a>
                        </div>
                    :null}

                </div>
                <div className="img-wrapper">
                    <img src={product.main_image} alt={product.title}/>
                </div>



                    {product.discount ? (
                        <div className="title">
                             <p>{product.title}</p>
                            <span>{product.get_price_function} {product.currency}</span>
                            <span className="old-price"><strike>{product.price} {product.currency}</strike></span>
                        </div>
                        ) : (
                            <div className="title">
                                <p>{product.title}</p>
                                <span>{product.get_price_function} {product.currency}</span>
                            </div>
                        )
                    }
                <div className="bottom-line">
                    {this.isInCart(product)}
                    {this.deliveryColor(product)}
                    <span className={`hearth pull-right ${product.is_favorite && `like`}`} data-product-id={product.id}><i className="glyphicon glyphicon-heart"></i></span>

                </div>
            </div>
        </div>

          )}
          </div>
    );
  }
});
ReactDOM.render(<Products />, document.getElementById('container'));
