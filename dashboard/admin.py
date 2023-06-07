from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(Patient)
admin.site.register(Bed)
admin.site.register(Turnover)


admin.site.register(Census)
# admin.site.register(Measures)
admin.site.register(Hiring)

@admin.register(Measures)
class MeasuresAdmin(admin.ModelAdmin):
    list_display = ('date_entered', 'hospital',  'readmissions', 'pressure_ulcer', 'against_medical_advice')
    
admin.site.register(FeedBack)
