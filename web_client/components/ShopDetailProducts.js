import React from 'react';
import createClass from 'create-react-class';
import AlertContainer from 'react-alert';


var ProductList = createClass({
  displayName: 'Product',

  showAlert: function(e) {
    console.log(e.target.getAttribute("data-message"));
    this.msg.show(e.target.getAttribute("data-message"), {
      time: 3000,
      type: 'success',
      icon: <img src="http://merp.mx/lib/css/icon/success-32.png" />
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

  AddOrRemoveFavorite: function(e) {
    e.preventDefault();
    var target = e.target || e.srcElement;
    var showAlert = this.showAlert(e);
    $.ajax({
            type: "GET",
            url: "/favorite/add",
            data: {
                'item': this.props.product.id
            },
            success: function (data) {
                if (data.created) {
                    target.parentElement.classList.toggle("like");
                    target.setAttribute('data-message', "Товар удален из избранных");
                }
                else {
                    target.parentElement.classList.remove("like");
                    target.setAttribute('data-message', "Товар добавлен в избранное");
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
      var target = e.target || e.srcElement;
      var showAlert = this.showAlert(e)
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
                      target.innerHTML = '<span class="glyphicon glyphicon-shopping-cart"></span>В корзине';
                      target.classList.toggle("in-the-basket");
                      target.setAttribute('data-message', "Товар успешно удален из корзины");
                  }
                  else if (data.deleted) {
                      target.innerHTML = '<span class="glyphicon glyphicon-shopping-cart"></span>Добавить в корзину';
                      target.classList.remove("in-the-basket");
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
    console.log(target.getAttribute("data-product-id"))
    $.ajax({
                url: '/product/change_publish_status/',
                type: 'GET',
                data: {
                    "item" : target.getAttribute("data-product-id"),
                },
                success: function (data) {
                    if(target.getAttribute("data-status") == "false") {
                      target.setAttribute('data-original-title', 'Скрытый');
                      target.setAttribute('data-status', "true");
                      target.setAttribute('data-message', "Товар успешно опубликован");
                      target.classList.remove('glyphicon-eye-open');
                      target.classList.toggle('glyphicon-eye-close');
                      target.parentElement.parentElement.parentElement.classList.toggle('active');
                    }
                    else {
                      target.setAttribute('data-original-title', 'Скрыть');
                      target.setAttribute('data-status', "false");
                      target.setAttribute('data-message', "Товар успешно скрыт");
                      target.classList.toggle('glyphicon-eye-open');
                      target.classList.remove('glyphicon-eye-close');
                      target.parentElement.parentElement.parentElement.classList.remove('active');
                    }

                }
            });
    var showAlert = this.showAlert(e);
  },

  inCart : function (product) {
    return (
        <a href="#" className="add-basket in-the-basket" data-product-id={this.props.product.id} data-message="Товар успешно удален из корзины" onClick={this.addOrRemoveFromCart}>
                      <span className="glyphicon glyphicon-shopping-cart"></span>
                      В корзине
                  </a>
    )
  },

  notInCart : function (product) {
    return (
        <a href="#" className="add-basket" data-product-id={this.props.product.id} data-message="Товар успешно добавлен в корзину" onClick={this.addOrRemoveFromCart}>
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

        <div className="col-md-4 col-sm-6">
        <AlertContainer ref={a => this.msg = a} {...alertOptions} />
          <div className={this.props.product.published ? "cover" : "cover active"}>
              <a className="url-item" href={this.props.product.detail_view}></a>
              <div className="top-line">

                  <h2>
                      <a href={this.props.product.detail_view}>
                      {this.props.product.shop}
                      </a>
                  </h2>
                  {this.props.product.is_owner ?
                      <div>
                          <a className="edited glyphicon glyphicon-cog" href={`/products/${this.props.product.slug}/update_product/`} data-toggle="tooltip" title="" data-placement="bottom" data-original-title="Редактировать"></a>
                          <a href="#" data-message={this.props.product.published ? "Товар успешно скрыт" : "Товар успешно опубликован"} className={`eye glyphicon glyphicon-eye-${this.props.product.published ? 'open' : 'close'}`} data-product-id={this.props.product.id} data-toggle="tooltip" title="" data-placement="bottom" data-original-title="Скрыть" data-status={`${this.props.product.published ? false : true}`} onClick={this.changePublishStatus}></a>
                          <a href="#" className="remove glyphicon glyphicon-remove-circle model-trigger"  data-url={this.props.product.delete_view} data-toggle="modal" data-target="#DeleteModal" title="" data-placement="bottom" data-product-id={this.props.product.id} data-original-title="Удалить" onClick={this.deleteProduct}></a>
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
                  <span className={`hearth pull-right ${this.props.product.is_favorite && `like`}`} data-product-id={this.props.product.id} onClick={this.AddOrRemoveFavorite}><i data-message={this.props.product.is_favorite ? "Товар удален из избранных" : "Товар добавлен в избранное"} className="glyphicon glyphicon-heart"></i></span>

              </div>
          </div>
      </div>
    )
  }
});

module.exports=ProductList;