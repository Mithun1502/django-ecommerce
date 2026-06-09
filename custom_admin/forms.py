from django import forms
from .models import Product
import re
import os

class ProductForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise forms.ValidationError(
                "Product name can contain only letters and spaces."
            )

        return name

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            allowed_extensions = [".jpg", ".jpeg", ".png"]
            ext = os.path.splitext(image.name)[1].lower()

            if ext not in allowed_extensions:
                raise forms.ValidationError("Only JPG, JPEG and PNG files are allowed.")

            if image.content_type not in ["image/jpeg", "image/png"]:
                raise forms.ValidationError("Only JPG, JPEG and PNG files are allowed.")

        return image

    class Meta:
        model = Product
        fields = "__all__"
