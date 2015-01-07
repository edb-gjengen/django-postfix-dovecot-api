from django.contrib import admin

from dpdapi.models import Alias, Domain, User


@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ['source', 'destination', 'active', 'domain']
    list_filter = ['domain']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass