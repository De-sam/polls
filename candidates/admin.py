from django.contrib import admin
from .models import Position, Candidate

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('surname', 'first_name', 'student_class', 'position')
    search_fields = ('surname', 'first_name', 'student_class')
    list_filter = ('position',)
