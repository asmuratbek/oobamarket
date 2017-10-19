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
                                    <img data-uk-cover src="img/template-magazin.jpg" alt=""/>
                                </div>
                            </div>
                            <div className="uk-transition-fade uk-position-cover uk-overlay uk-overlay-default">
                                <a href="" className="uk-position-cover">{}</a>
                                <h4 className="uk-margin-remove">Magazin name</h4>
                                <div className="control">
                                    <p className="phone"><span className="uk-margin-small-right" data-uk-icon="icon: phone"></span>0550 475588 0550 475588 0550 475588</p>
                                    <p className="email"><span className="uk-margin-small-right" data-uk-icon="icon: mail"></span> example@mail.com</p>
                                </div>
                            </div>
                        </div>
                        <div className="uk-padding-small uk-grid uk-margin-remove footer">
                            <h4 className="uk-width-1-2@l uk-width-3-5@m uk-padding-remove"> Империя Спорта  Империя Спорта </h4>
                            <div className="subscribe uk-width-1-2@l uk-width-2-5@m uk-padding-remove"><a href="">Подписаться</a></div>
                        </div>
                    </div>
                </div>
        )
    }
}

export default Shop;
