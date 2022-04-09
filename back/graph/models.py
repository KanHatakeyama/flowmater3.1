from django.db import models
import os
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

# Create your models here.

default_graph = '[{"id":"l1g63q47","type":"Task","width":125,"height":75,"x":255,"y":90,"name":"start"}]'


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Graph(models.Model):

    def __str__(self) -> str:
        return self.title

    title = models.CharField(max_length=200, default="title")
    tags = models.CharField(
        max_length=2000, default="new", blank=True, null=True)
    p_tags = models.ManyToManyField("Tag", blank=True)
    graph = models.TextField(null=True, blank=True, default=default_graph)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # override save

    def save(self, *args, **kwargs):

        # reset tags
        try:
            self.p_tags.clear()
            # add manytomany tags for django
            tag_list = set(self.tags.split(","))
            for tag_name in tag_list:
                found_tag = list(Tag.objects.filter(
                    name__iexact=tag_name).values())

                # make a new tag if not available
                if len(found_tag) == 0:
                    found_tag = Tag.objects.create(name=tag_name)
                else:
                    found_tag = found_tag[0]["id"]
                self.p_tags.add(found_tag)
        except:
            pass
        super().save(*args, **kwargs)


class FileSizeValidator:
    def __init__(self, val: float, byte_type="mb"):
        assert byte_type in ["b", "kb", "mb", "gb"]
        if byte_type == "b":
            self._upper_byte_size = val
        elif byte_type == "kb":
            self._upper_byte_size = 1000 * val
        elif byte_type == "mb":
            self._upper_byte_size = (1000 ** 2) * val
        elif byte_type == "gb":
            self._upper_byte_size = (1000 ** 3) * val
        self._err_message = f"size should less than {val}{byte_type.upper()}"

    def __call__(self, file_val: UploadedFile):
        byte_size = file_val.size
        if byte_size > self._upper_byte_size:
            raise ValidationError(message=self._err_message)


class MediaFile(models.Model):

    def __str__(self) -> str:
        return self.filename()

    def filename(self):
        return os.path.basename(self.upload.name)

    upload = models.FileField(upload_to='uploaded/',
                              #  validators=[FileSizeValidator(val=10, byte_type="mb")],
                              )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
