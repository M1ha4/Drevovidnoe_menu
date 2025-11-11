from django.db import models
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ValidationError



class Menu(models.Model):
    name = models.SlugField(max_length=100, unique=True, help_text="machine name, used to draw the menu")
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.title or self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text="Order among siblings")
    # Two options to specify where the link goes:
    url = models.CharField(max_length=500, blank=True, help_text="Absolute or relative URL, e.g. /about/ or https://...")
    named_url = models.CharField(max_length=255, blank=True, help_text="Django named URL (reverse name).")
    named_url_kwargs = models.JSONField(blank=True, null=True, default=dict,
                                        help_text="JSON object for kwargs passed to reverse, e.g. {\"pk\": 3}")

    class Meta:
        ordering = ['menu', 'order', 'id']

    def __str__(self):
        return f"{self.title} ({self.menu.name})"

    def clean(self):
        if not (self.url or self.named_url):
            raise ValidationError("Either `url` or `named_url` must be set.")

    def get_resolved_url(self):
        """
        Returns resolved absolute path or value for comparison.
        If named_url is present, try reverse; if fails, return '#'.
        """
        if self.named_url:
            try:
                return reverse(self.named_url, kwargs=self.named_url_kwargs or {})
            except NoReverseMatch:
                # Failing reverse — still return placeholder (or keep as-is)
                return '#'
        return self.url or '#'
