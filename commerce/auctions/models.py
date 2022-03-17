from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Bid(models.Model):
    price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="price")

    def __str__(self):
        return f" {self.price} from {self.user}"
    
class Listing(models.Model):
    title = models.CharField(max_length=64)
    describtion = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing", blank=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing", default=0)
    image_url = models.CharField(max_length=800)
    watchlist = models.ManyToManyField(User, related_name="watchlistings", blank=True)
    category = models.CharField(max_length=400, blank=True)
    closed = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.title} : {self.price}"


class Comment(models.Model):
    comment = models.CharField(max_length=800)
    writer  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    