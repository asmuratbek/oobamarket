import React, {Component} from 'react';

class Product extends Component {

    AddOrRemoveFavorite = (e) => {
        e.preventDefault();
        console.log('fav')
    };

    addOrRemoveFromCart = (e) => {
        e.preventDefault();
        console.log('cart')
    };

    changePublishStatus = (e) => {
        e.preventDefault();
        console.log('pub')
    };

    isInCart = (product) => {
        return this.props.cartItems.indexOf(product.pk) !== -1
    };

    isInFavorites = (product) => {
        return this.props.favorites.indexOf(product.pk) !== -1
    };

    handleDelete = (product_id) => {
        console.log('delete')
    };

    deleteProduct = (e) => {
        e.preventDefault();
        console.log('do del')
    };

    render () {
        return (
            <div className="uk-grid-match">
        <div className="shadow uk-text-center">
            <div className="setting">
                <a href={`${this.props.product.detail_view}${this.props.product.slug}/update-product/`}
                   data-uk-icon="icon: file-edit" title="Редактировать товар" data-uk-tooltip></a>
                <a className={`product-vision ${!this.props.product.published && ' disabled'}`} href="#"
                   data-uk-icon="icon: copy" title={this.props.product.published ? "Скрыть товар" : "Опубликовать товар"} data-uk-tooltip
                data-item-id={this.props.product.pk}></a>
                <a href="#" data-uk-icon="icon: close" title="Удалить товар" data-uk-tooltip
                data-item-id={this.props.product.pk}></a>
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
                    <a href={this.props.product.detail_view} className="uk-position-cover"></a>
                    <small className="uk-display-block">Магазин</small>
                    <h4 className="uk-margin-remove"><a href="#">{this.props.product.shop}</a></h4>
                    <p>{this.props.product.short_description}</p>
                    <div className="control">
                        <a href="#" className={`favorite uk-margin-medium-right ${this.isInFavorites(this.props.product) && 'like'}`}
                           title={this.isInFavorites(this.props.product) ? 'Удалить из избранных' : 'Добавить в избранное'} data-uk-tooltip
                           data-item-id={this.props.product.pk}><span
                                className=" uk-icon" data-uk-icon="icon: heart; ratio: 2"></span></a>
                        <a href="#" className={`basket cart uk-margin-medium-left ${this.isInCart(this.props.product) && 'in'}`}
                           title={this.isInCart(this.props.product) ? 'В корзине' : 'Добавить в корзину'} data-uk-tooltip
                        data-item-id={this.props.product.pk}><span
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
}

export default Product;
