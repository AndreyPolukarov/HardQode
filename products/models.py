from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    duration = models.PositiveIntegerField()
    products = models.ManyToManyField(Product)


class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched_time = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=[("Пр", "Просмотрено"), ("НП", "Не просмотрено")])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        total_duration = self.lesson
        if self.watched_time / total_duration >= 0.8:
            self.status = "Пр"
        else:
            self.status = "НП"
        super().save(*args, **kwargs)

