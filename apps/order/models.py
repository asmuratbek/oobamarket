from decimal import Decimal
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
# Create your models here.
from django.template.loader import get_template, render_to_string

from apps.cart.models import Cart
from apps.product.models import Product
from apps.shop.models import Shop
from apps.users.models import User
from apps.utils.models import PublishBaseModel


import braintree

if settings.DEBUG:
    braintree.Configuration.configure(braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC,
        private_key=settings.BRAINTREE_PRIVATE)


class UserCheckout(models.Model):
    user = models.OneToOneField(User, null=True, blank=True) #not required
    email = models.EmailField(unique=True) #--> required
    braintree_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.email

    @property
    def get_braintree_id(self, ):
        instance = self
        if not instance.braintree_id:
            result = braintree.Customer.create({
                "email": instance.email,
            })
            if result.is_success:
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id

    def get_client_token(self):
        customer_id = self.get_braintree_id
        if customer_id:
            client_token = braintree.ClientToken.generate({
                "customer_id": customer_id
            })
            return client_token
        return None


def update_braintree_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        instance.get_braintree_id


post_save.connect(update_braintree_id, sender=UserCheckout)


ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)

    def __str__(self):
        return self.street

    def get_address(self):
        return "%s, %s, %s %s" %(self.street, self.city, self.state, self.zipcode)


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout, null=True)
    billing_address = models.ForeignKey(UserAddress, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', null=True)
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
    order_total = models.DecimalField(max_digits=50, decimal_places=2, )
    order_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.cart.id)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse("order:detail", kwargs={"pk": self.pk})

    def mark_completed(self, order_id=None):
        self.status = "paid"
        if order_id and not self.order_id:
            self.order_id = order_id
        self.save()


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total

pre_save.connect(order_pre_save, sender=Order)


class SimpleOrder(PublishBaseModel):

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)
    cart = models.ForeignKey(Cart, blank=True, null=True)

    def __str__(self):
        return  str(self.name) + str(self.last_name)



def send_email_to_shop_owner(sender, instance, *args, **kwargs):
    template_html = 'account/email/email_confirmation_signup_message.html'
    template_text = 'account/email/email_confirmation_signup_message.txt'
    # text = get_template(template_text)
    # html = get_template(template_html)
    # # d = Context({'n': '123131', 'email': 'asdasda'})
    # text_content = text.render(d)
    # html_content = html.render(d)
    shops = instance.cart.get_shops()
    for shop in shops:
        products = Product.objects.filter(shop=shop, cartitem__cart=instance.cart)
        text_content = render_to_string(template_text,
                                        {"user": shop.user.first, "text": 'sdadsad', 'date': 'dsadad',
                                         'email': 'dasda'})
        html_content = render_to_string(template_html,
                                        {"name": instance.name + ' ' + instance.last_name,
                                         'date': instance.created_at, 'address': instance.address,
                                         'phone': instance.phone,
                                         'products': products,
                                         })

        msg = EmailMultiAlternatives('Поступил новый заказ в магазин ' + shop.title, text_content, settings.EMAIL_HOST_USER, [shop.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()
    # name = str(instance.name) + "\n" if instance.name else ""
    # last_name = str(instance.last_name) + "\n" if instance.last_name else ""
    # phone = str(instance.phone) + "\n"
    # address = str(instance.address) + "\n"
    # shops = instance.cart.get_shops()
    # for shop in shops:
    #     products = Product.objects.filter(shop=shop, cartitem__cart=instance.cart)
    #     message = ""
    #     for product in products:
    #         message += str(product.title) + " Количество: " + str(product.cartitem_set.get(cart=instance.cart).quantity) + "\n"
    #
    #     shop.send_email("Вам поступил новый заказ в магазин " + shop.title,
    #                     name + last_name + phone + address + message
    #                     )

post_save.connect(send_email_to_shop_owner, sender=SimpleOrder)
