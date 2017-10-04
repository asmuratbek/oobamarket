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
                'item': this.props.product.pk
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
                  "item":  this.props.product.pk
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

  // inCart : function (product) {
  //   return (
  //       <span className="glyphicon glyphicon-shopping-cart enable" data-toggle="tooltip"
  //             data-placement="top" data-product-id={this.props.product.id}
  //                         data-tip="В корзине" onClick={this.addOrRemoveFromCart}></span>
  //   )
  // },
  //
  // notInCart : function (product) {
  //   return (
  //       <span className="glyphicon glyphicon-shopping-cart" data-toggle="tooltip"
  //             data-placement="top" data-product-id={this.props.product.id}
  //                         data-tip="Добавить в корзину" onClick={this.addOrRemoveFromCart}></span>
  //   )
  // },

  isInCart : function (product) {
      return this.props.cartItems.indexOf(product.pk) !== -1
  },

  isInFavorites: function (product) {
      return this.props.favorites.indexOf(product.pk) !== -1
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
        <div className="uk-grid-match">
    <div className="shadow uk-text-center">
        <div className="setting">
            <a href="" data-uk-icon="icon: file-edit" title="Редактировать товар" data-uk-tooltip></a>
            <a className="product-vision" href="" data-uk-icon="icon: copy" title="Скрыть товар" data-uk-tooltip></a>
            <a href="" data-uk-icon="icon: close" title="Удалить товар" data-uk-tooltip></a>
        </div>
        <div className="uk-inline-clip uk-transition-toggle">
            <div className="border">
                <a href="" className="uk-position-cover"></a>
                <div className="uk-cover-container">
                    <canvas width="400" height="500"></canvas>
                    <img data-uk-cover src={this.props.product.main_image} alt=""/>
                </div>
            </div>
            <div className="uk-transition-fade uk-position-cover uk-overlay uk-overlay-default">
                <a href="" className="uk-position-cover"></a>
                <small className="uk-display-block">Магазин</small>
                <h4 className="uk-margin-remove"><a href="##">{this.props.product.shop}</a></h4>d
                <p>{this.props.product.short_description}</p>
                <div className="control">
                    <a href="#" className={`favorite uk-margin-medium-right ${this.isInFavorites(this.props.product) && 'like'}`} title="Добавить в избранные" data-uk-tooltip
                    onClick={this.AddOrRemoveFavorite}><span
                            className=" uk-icon" data-uk-icon="icon: heart; ratio: 2"></span></a>
                    <a href="#" className={`basket uk-margin-medium-left ${this.isInCart(this.props.product) && 'in'}`} title="Добавить в корзину" data-uk-tooltip
                    onClick={this.addOrRemoveFromCart}><span
                            className=" uk-icon" data-uk-icon="icon: cart; ratio: 2"></span></a>
                </div>
            </div>
        </div>
        <div className="uk-padding-small uk-grid uk-margin-remove footer">
            <h4 className="uk-width-3-5@l uk-width-3-5@m uk-padding-remove">{this.props.product.title}</h4>
            <div className="uk-width-2-5@l uk-width-2-5@m uk-padding-remove">
                <p >{this.props.product.get_price_function} сом </p>
            </div>
        </div>
    </div>
</div>

    )
  }
});

module.exports=ProductList;
