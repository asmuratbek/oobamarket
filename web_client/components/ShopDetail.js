import React from 'react';
import createClass from 'create-react-class';


var ShopDetail = createClass({
  displayName: 'ShopDetail',

  render: function(){
    return(
            <div className="col-md-3 col-sm-6 new-design">
                            <div className="single-magazin new-design">
                                <div className="img-wrapper ">

                                    <img src={this.props.shop.logo} alt={this.props.shop.title} />

                                    <div className="back-fade">

                                        <a className="url" href={this.props.shop.get_absolute_url}></a>

                                        <div className="name-magazin-title">
                                            <h3>{this.props.shop.title}</h3>
                                        </div>

                                        <div className="info">
                                            {this.props.shop.phone ? (
                                                <div>
                                                    <a href={`tel: ${this.props.shop.phone}`} className="">
                                                        <span className="glyphicon glyphicon-earphone"></span>
                                                        {this.props.shop.phone}
                                                    </a>
                                                </div>
                                            )
                                            : (

                                                <div>
                                                    <a href="tel: 0312 89 53 33" className="">
                                                        <span className="glyphicon glyphicon-earphone"></span>
                                                        не указан
                                                    </a>
                                                </div>
                                                )}

                                            <div>
                                                <a href={`mailto: ${this.props.shop.email}`} className="">
                                                    <span className="glyphicon glyphicon-envelope"></span>
                                                    {this.props.shop.email}
                                                </a>
                                            </div>
                                        </div>

                                        <div className="bottom-line">
                                            <div className="col-md-6">
                                                <h3> {this.props.shop.title} </h3>
                                            </div>
                                            <div className="col-md-6">
                                                {this.props.shop.is_owner ? (
                                                    ""
                                                ):(
                                                    <a className={`subscribe_shop ${this.props.shop.is_subscribed ? 'disabled' : 'enable'}`}>
                                                        {this.props.shop.is_subscribed ? "Отписаться" : "Подписаться" }</a>
                                                )}
                                            </div>
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
    )
  }
});

module.exports=ShopDetail;

