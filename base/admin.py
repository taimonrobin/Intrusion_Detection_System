from django.contrib import admin
from .models import SourceAddr, DestinationAddr, UniqueSourceAddr, UniqueDestinationAddr
# Register your models here.

admin.site.register(SourceAddr)
admin.site.register(DestinationAddr)
admin.site.register(UniqueSourceAddr)
admin.site.register(UniqueDestinationAddr)
