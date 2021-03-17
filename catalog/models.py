from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import timezone
#from phone_field import PhoneField
#from phonenumber_field.modelfields import PhoneNumberField


CATEGORY_CHOICES = (
	('Vegetables','Vegetables'),
	('Electronics','Electronics'),
	('Fruits','Fruits'),
	('Detergents','Detergents'),
	('Spices','Spices'),
	('Eggs','Eggs'),
	('Perfumes','Perfumes'),
	('Neckless','Neckless'),
	('Beads','Beads'),
	('Earings','Earings')
)

LABEL_CHOICES = (
	('S','secondary'),
	('P','primary'),
	('D','danger'),
    ('I','info')
)

class Item(models.Model):
	title = models.CharField(max_length=200)
	price = models.IntegerField()
	discount_price = models.IntegerField(blank=True, null=True)
	slug =  models.SlugField()
	status = models.CharField(max_length=200)
	category = models.CharField(choices=CATEGORY_CHOICES,max_length=15)
	label  = models.CharField(choices=LABEL_CHOICES,max_length=2)
	description = models.TextField()
	image = models.ImageField(upload_to='static/images', height_field=None, width_field=None, max_length=100,default='default.jpg')

	def __str__(self):
		return self.title

	def get_add_to_cart_url(self):
		return reverse( 'add_to_cart',kwargs={'slug':self.slug})

	def get_remove_from_cart_url(self):
		return reverse( 'remove_from_cart',kwargs={'slug':self.slug})



class OrderItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item,on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} of {self.item.title}"

	def get_total_item_price(self):
		return self.quantity * self.item.price

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_final_price()


	def get_total_item_discount_price(self):
		return self.quantity * self.item.discount_price

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_item_discount_price()
		return self.get_total_item_price()


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	#hostel = models.CharField(max_length=255,default="Runda")
	#phoneNumber = PhoneNumberField()
	items = models.ManyToManyField(OrderItem)
	ordered = models.BooleanField(default=False)
	start_date = models.DateTimeField( auto_now_add=True)
	ordered_date = models.DateTimeField()

	def __str__(self):
		return self.user.username

def get_total(self):
	total = 0
	for order_item in self.items.all():
		total +=order_item.get_final_price()
	return total

class slider(models.Model):
	image = models.ImageField(upload_to='slider')
	heading = models.CharField(max_length=255)
	#button = models.CharField(max_length=255)
	slug =  models.SlugField(default='item')
	category = models.CharField(choices=CATEGORY_CHOICES,max_length=15,default='Food')
	description = models.TextField()

	def __str__(self):
		return self.category


class addition_info(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	slug =  models.SlugField(default='Food')
	images = models.ImageField(upload_to='addition_info')
	descriptions = models.TextField(blank=True)

	def __str__(self):
		return self.slug

class about(models.Model):
	image = models.ImageField(upload_to='about')
	title1 =  models.CharField(max_length=200)
	description1 =  models.TextField()
	title2 =  models.CharField(max_length=200)
	description2 =  models.TextField()

	def __str__(self):
		return self.title1

class about1(models.Model):
	image = models.ImageField(upload_to='about')



class contact(models.Model):
	name  = models.CharField(max_length=255, null=True)
	email = models.EmailField(max_length=255, null=False, blank=True)
	subject = models.CharField(max_length=255,null=False)
	message = models.TextField( null=False)

	def __str__(self):
		return self.name


class delivery(models.Model):
	#user = models.ForeignKey(User, on_delete=models.CASCADE)
	hostel = models.CharField(max_length=255)
	phoneNumber = models.IntegerField()
	delivered_at = models.CharField(max_length=255,null=False)

	def __str__(self):
		return self.hostel



#new models for the changes on recent products

class Recent_Products(models.Model):
	product_name = models.CharField(max_length=222)
	image = models.ImageField(upload_to='recent_products')
	price = models.DecimalField(max_digits=7, decimal_places=4)
	liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
	
	def num_likes(self):
		return self.liked.all().count()


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Recent_Products, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Unlike', max_length=10)
    date_liked = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.product)


#new models for the changes on customer reviews

class Rate(models.Model):
    listing = models.ForeignKey(Recent_Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rate = models.IntegerField(null=True, blank=True)


class Customer_Reviews(models.Model):
	listing = models.ForeignKey(Rate,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	profession = models.CharField(max_length=222)
	message = models.TextField()


