from django.contrib import admin
from .models import Company, Catalog, CatalogItem, CatalogItemTranslation

admin.site.register(Company)
admin.site.register(Catalog)
admin.site.register(CatalogItem)
admin.site.register(CatalogItemTranslation)

