from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from lms.models import Author, Book, Category, Course, Fine, IssueBook, Student, User

admin.site.register(Author)
admin.site.register(Course)
admin.site.register(IssueBook)
admin.site.register(Book)
admin.site.register(Fine)
admin.site.register(Category)
admin.site.register(Student)

# @admin.register(User)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ["id", "full_name", "email", "roll_no", "course"]
#     readonly_fields = ['password']


class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("User Info", {"fields": ("full_name",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        # ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
# # Now register the new UserAdmin...
# admin.site.register(User, UserAdmin)

# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ('email', 'full_name', 'is_active', 'is_staff')
#     search_fields = ('email', 'full_name')
#     ordering = ('email',)

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('full_name',)}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'full_name', 'password1', 'password2'),
#         }),
#     )

# admin.site.register(User, CustomUserAdmin)
