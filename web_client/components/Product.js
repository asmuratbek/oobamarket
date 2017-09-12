import React from 'react';
import createClass from 'create-react-class';
import AlertContainer from 'react-alert';
import $ from 'jquery';
import ReactTooltip from 'react-tooltip';


var ProductList = createClass({
  displayName: 'Product',

  showAlert: function(e) {
    console.log(e.target.getAttribute("data-message"));
    this.msg.show(e.target.getAttribute("data-message"), {
      time: 3000,
      type: 'success',
      icon: <img src="http://merp.mx/lib/css/icon/success-32.png" alt='' />
    })
  },

  // render () {
  //   return (
  //     <div>
  //       <AlertContainer ref={a => this.msg = a} {...this.alertOptions} />
  //       <button onClick={this.showAlert}>Show Alert</button>
  //     </div>
  //   )
  // }

  deliveryColor: function(product) {
      if (this.props.product.delivery_type === 'paid') {
          return (
              <span className="truck pull-right yellow" data-toggle="tooltip" title=""
                        data-placement="top" data-original-title={this.props.product.delivery_type_display}><i className="fa fa-truck" aria-hidden="true"></i></span>
          )
      }
      else if (this.props.product.delivery_type === 'free') {
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

  AddOrRemoveFavorite: function(e) {
    e.preventDefault();
    var showAlert = this.showAlert(e);
    var target = e.target || e.srcElement;
    $.ajax({
            type: "GET",
            url: "/favorite/add",
            data: {
                'item': this.props.product.id
            },
            success: function (data) {
                if (data.created) {
                    target.classList.toggle("enable");
                    target.classList.toggle("like");
                    target.setAttribute('data-message', "Товар удален из избранных");
                    target.setAttribute('data-tip', "Удалить из избранных");
                }
                else {
                    target.classList.remove("enable");
                    target.classList.remove("like");
                    target.setAttribute('data-message', "Товар добавлен в избранное");
                    target.setAttribute('data-tip', "Добавить в избранное");
                }
                $('.favorites_count').text(data.favorites_count)
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
  },

  addOrRemoveFromCart : function (e) {
      e.preventDefault();
      var showAlert = this.showAlert(e);
      var target = e.target || e.srcElement;
      $.ajax({
          type: "GET",
          url: "/cart/",
          data:
              {
                  "item":  this.props.product.id
              },
          success: function (data) {
              $('.cart-count').text(data.total_items);
              if (data.item_added) {
                      target.classList.toggle("enable");
                      target.setAttribute('data-tip', "В корзине");
                      target.setAttribute('data-message', "Товар успешно удален из корзины");
                  }
                  else if (data.deleted) {
                      target.classList.remove("enable");
                      target.setAttribute('data-tip', "Добавить в корзину");
                      target.setAttribute('data-message', "Товар успешно добавлен в корзину");
                  }
          },
          error: function (response, error) {
              console.log(response);
              console.log(error);
          }
      });
  },

  changePublishStatus: function(e) {
    e.preventDefault();
    var target = e.target || e.srcElement;
    console.log(target.getAttribute("data-product-id"));
    $.ajax({
                url: '/product/change_publish_status/',
                type: 'GET',
                data: {
                    "item" : target.getAttribute("data-product-id"),
                },
                success: function (data) {
                    if(target.getAttribute("data-status") == "false") {
                      target.setAttribute('data-tip', 'Опубликовать');
                      target.setAttribute('data-message', "Товар успешно опубликован");
                      target.setAttribute('data-status', 'true');
                      target.classList.remove('glyphicon-eye-open');
                      target.classList.toggle('glyphicon-eye-close');
                      target.parentElement.parentElement.classList.toggle('disabled');
                    }
                    else {
                      target.setAttribute('data-tip', 'Скрыть');
                      target.setAttribute('data-message', "Товар успешно скрыт");
                      target.setAttribute('data-status', 'false');
                      target.classList.toggle('glyphicon-eye-open');
                      target.classList.remove('glyphicon-eye-close');
                      target.parentElement.parentElement.classList.remove('disabled');
                    }

                }
            });
    var showAlert = this.showAlert(e);
  },

  inCart : function (product) {
    return (
        <span className="glyphicon glyphicon-shopping-cart enable" data-toggle="tooltip"
              data-placement="top" data-product-id={this.props.product.id}
                          data-tip="В корзине" onClick={this.addOrRemoveFromCart}></span>
    )
  },

  notInCart : function (product) {
    return (
        <span className="glyphicon glyphicon-shopping-cart" data-toggle="tooltip"
              data-placement="top" data-product-id={this.props.product.id}
                          data-tip="Добавить в корзину" onClick={this.addOrRemoveFromCart}></span>
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

  handleDelete: function(product_id){
    this.props.onProductDelete(product_id)
  },

  deleteProduct: function(e) {
    e.preventDefault();
    var handleDelete = this.handleDelete;
    var product_id = e.target.getAttribute('data-product-id')
    function initForm() {
        $('#ProductDelete').on('submit', function (event) {
            event.preventDefault();
            // $("#DeleteModal").fadeOut();
            $("#DeleteModal").modal('hide');
            var that = this;
            $(that).addClass('hidden');
            $.ajax({
                method: 'POST',
                dataType: 'JSON',
                data: $(that).serialize(),
                url: $(that).attr('action'),
                success: function (response) {
                },
                error: function (error) {
                }
            });
            handleDelete(product_id);
        });
    }

    var target = e.target;
    var link = target.getAttribute('data-url');

    $.ajax({
        method: 'GET',
        dataType: 'HTML',
        url: link,
        success: function (response) {
            $('#ajax-modal-body').html(response);
            initForm();
            $('#application-form').append("{% csrf_token %}");

        },
        error: function () {

        }
    });
  },

  render: function(){

    var alertOptions = {
      offset: 14,
      position: 'bottom left',
      theme: 'light',
      time: 5000,
      transition: 'scale',
    }
    return (

        <div className="col-md-3 col-sm-6 new-design">
            <AlertContainer ref={a => this.msg = a} {...alertOptions} />
        <div className={this.props.product.published ? "img-wrapper" : "img-wrapper disabled"}>
            {this.props.product.is_owner ?

            <div className="setting-control">
                <a href={`/product/${this.props.product.slug}/update-product/`} className="glyphicon glyphicon-pencil"
                   data-toggle="tooltip" title="" data-placement="top"
                          data-tip="Редактировать товар"></a>
                <ReactTooltip/>
                <a href="#" data-message={this.props.product.published ? "Товар успешно скрыт" : "Товар успешно опубликован"}
                             className={`eye glyphicon glyphicon-eye-${this.props.product.published ? 'open' : 'close'}`}
                             data-product-id={this.props.product.id} data-toggle="tooltip" title="" data-placement="bottom"
                             data-tip="Скрыть" data-status={`${this.props.product.published ? false : true}`}
                             onClick={this.changePublishStatus}></a>
                <ReactTooltip/>
                <a href="#" className="remove glyphicon glyphicon-remove model-trigger"
                             data-url={this.props.product.delete_view} data-toggle="modal" data-target="#DeleteModal" title=""
                             data-placement="bottom" data-product-id={this.props.product.id} data-tip="Удалить"
                             onClick={this.deleteProduct}></a>
                <ReactTooltip/>

            </div>
                : ''}

                <img src={this.props.product.main_image} alt={this.props.product.title}/>

            <div className="back-fade">

                <a href={this.props.product.detail_view}></a>

                <div className="name-magazin-title">
                    <h3>
                        <small>Магазин</small>
                        {this.props.product.shop}
                    </h3>
                    <p>{this.props.product.short_description}</p>
                </div>

                <div className="button-basket-favorite">
                    {this.isInCart(this.props.product)}
                    <span className={`glyphicon glyphicon-heart ${this.props.product.is_favorite && 'enable like'}`}
                          data-product-id={this.props.product.id} data-toggle="tooltip" title=""
                          data-placement="top"
                          data-tip={this.props.product.is_favorite ? "Удалить из избранных" : "Добавить в избранное"}
                        onClick={this.AddOrRemoveFavorite}></span>
                    <ReactTooltip/>
                </div>

                <div className="title-price">
                    <div className="col-md-8">
                        <h4>{this.props.product.title}</h4>
                    </div>

                          {this.props.product.discount ? (
                              <div className="col-md-4">
                                  <span>{this.props.product.get_price_function} {this.props.product.currency}</span>
                                  <span><strike>{this.props.product.price} {this.props.product.currency}</strike></span>
                              </div>
                      ) : (
                              <div className="col-md-4">
                                <span>{this.props.product.get_price_function} {this.props.product.currency}</span>
                              </div>
                      )
                  }

                </div>

            </div>
        </div>
    </div>

    )
  }
});

module.exports=ProductList;
