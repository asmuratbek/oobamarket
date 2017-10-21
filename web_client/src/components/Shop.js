import React, {Component} from 'react'

class Shop extends Component {
    render () {
        return (
            <div className="uk-grid-match">
                    <div className="shadow uk-text-center uk-transition-toggle">
                        <div className="uk-inline-clip uk-transition-toggle">
                            <div className="border">
                                <div className="uk-cover-container">
                                    <canvas width="400" height="500">{}</canvas>
                                    <img data-uk-cover src={this.props.shop.logo} alt={this.props.shop.title}/>
                                </div>
                            </div>
                            <div className="uk-transition-fade uk-position-cover uk-overlay uk-overlay-default">
                                <a href={this.props.shop.get_absolute_url} className="uk-position-cover"></a>
                                <h4 className="uk-margin-remove">{this.props.shop.title}</h4>
                                <div className="control">
                                    <p className="phone"><span className="uk-margin-small-right" data-uk-icon="icon: phone"></span>{this.props.shop.phone ? (
                                        this.props.shop.phone
                                    ): "Не указан"}</p>
                                    <p className="email"><span className="uk-margin-small-right" data-uk-icon="icon: mail"></span> {this.props.shop.email}</p>
                                </div>
                            </div>
                        </div>
                        <div className="uk-padding-small uk-grid uk-margin-remove footer">
                            <h4 className="uk-width-1-2@l uk-width-3-5@m uk-padding-remove"> {this.props.shop.title} </h4>
                            <div className="subscribe uk-width-1-2@l uk-width-2-5@m uk-padding-remove">
                                {this.props.shop.is_owner ? (
                                                    ""
                                                ):(
                                                    <a href="">{this.props.shop.is_subscribed ? "Подписаны" : "Подписаться" }</a>
                                                )}

                            </div>
                        </div>
                    </div>
                </div>
        )
    }
}

export default Shop;
