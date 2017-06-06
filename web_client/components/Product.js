import React from 'react'
import createClass from 'create-react-class'


var ProductList = createClass({
  displayName: 'ProductList',

  deliveryColor: function(product) {
      if (this.props.product.delivery_type == 'paid') {
          return (
              <span className="truck pull-right yellow" data-toggle="tooltip" title=""
                        data-placement="top" data-original-title={this.props.product.delivery_type_display}><i className="fa fa-truck" aria-hidden="true"></i></span>
          )
      }
      else if (this.props.product.delivery_type == 'free') {
          return (
              <span className="truck pull-right green" data-toggle="tooltip" title=""
                        data-placement="top" data-original-title={this.props.product.delivery_type_display}><i className="fa fa-truck" aria-hidden="true"></i></span>
          )
      }
      else {
          return (
              <span className="truck pull-right" data-toggle="tooltip" title=""
                        data-placement="top" data-original-title={this.props.product.delivery_type_display}><i className="fa fa-truck" aria-hidden="true"></i></span>
          )
      }
  },

  addOrRemoveFromCart : function (product) {

      $.ajax({
          type: "GET",
          url: "/cart/",
          data:
              {
                  "item":  this.props.product.id
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
        <a className="add-basket in-the-basket" data-product-id={this.props.product.id} onClick={() => this.addOrRemoveFromCart(product)}>
                      <span className="glyphicon glyphicon-shopping-cart"></span>
                      В корзине
                  </a>
    )
  },

  notInCart : function (product) {
    return (
        <a className="add-basket" data-product-id={this.props.product.id} onClick={() => this.addOrRemoveFromCart(product)}>
                      <span className="glyphicon glyphicon-shopping-cart"></span>
                      Добавить в корзину
                  </a>
    )
  },

  isInCart : function (product) {
      if (this.props.product.is_in_cart) {
          return (
              this.inCart(product)
          )
      } else {
          return (
              this.notInCart(product)
          )
      }
  },

  render: function(){
    return (

        <div className="col-md-3 col-sm-6">
          <div className="cover">
              <a className="url-item" href={this.props.product.detail_view}></a>
              <div className="top-line">

                  <h2>
                      <a href={this.props.product.detail_view}>
                      {this.props.product.shop_title}
                      </a>
                  </h2>
                  {this.props.product.is_owner ?
                      <div>
                          <a className="edited glyphicon glyphicon-cog" href={`/products/${this.props.product.slug}/update_product/`} data-toggle="tooltip" title="" data-placement="bottom" data-original-title="Редактировать"></a>
                          <a className={`eye glyphicon glyphicon-eye-${this.props.product.published ? 'open' : 'close'}`} data-toggle="tooltip" title="" data-placement="bottom" data-original-title="Скрыть" data-status={`${this.props.product.published ? false : true}`}></a>
                          <a className="remove glyphicon glyphicon-remove-circle model-trigger"  data-url={this.props.product.delete_url} data-toggle="modal" data-target="#DeleteModal" title="" data-placement="bottom" data-original-title="Удалить"></a>
                      </div>
                  :null}

              </div>
              <div className="img-wrapper">
                  <img src={this.props.product.main_image} alt={this.props.product.title}/>
              </div>



                  {this.props.product.discount ? (
                      <div className="title">
                           <p>{this.props.product.title}</p>
                          <span>{this.props.product.get_price_function} {this.props.product.currency}</span>
                          <span className="old-price"><strike>{this.props.product.price} {this.props.product.currency}</strike></span>
                      </div>
                      ) : (
                          <div className="title">
                              <p>{this.props.product.title}</p>
                              <span>{this.props.product.get_price_function} {this.props.product.currency}</span>
                          </div>
                      )
                  }
              <div className="bottom-line">
                  {this.isInCart(this.props.product)}
                  {this.deliveryColor(this.props.product)}
                  <span className={`hearth pull-right ${this.props.product.is_favorite && `like`}`} data-product-id={this.props.product.id}><i className="glyphicon glyphicon-heart"></i></span>

              </div>
          </div>
      </div>
    )
  }
});

module.exports=ProductList;
