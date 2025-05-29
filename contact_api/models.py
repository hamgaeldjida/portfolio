from django.db import models
import user_agents

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ['-created_at']

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device = models.CharField(max_length=255, blank=True)
    browser = models.CharField(max_length=255, blank=True)
    os = models.CharField(max_length=255, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.device} - {self.visited_at}"

    class Meta:
        ordering = ['-visited_at']

    def save(self, *args, **kwargs):
        if self.user_agent:
            ua = user_agents.parse(self.user_agent)
            self.device = f"{ua.device.family} {ua.device.brand} {ua.device.model}".strip()
            self.browser = f"{ua.browser.family} {ua.browser.version_string}".strip()
            self.os = f"{ua.os.family} {ua.os.version_string}".strip()
        super().save(*args, **kwargs)
