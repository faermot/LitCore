from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Genre, Author, Book, BuyLink, Favorite


class ColorInput(forms.TextInput):
    input_type = 'color'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({
            'style': 'width:52px;height:34px;padding:2px;border:1px solid #ccc;'
                     'border-radius:4px;cursor:pointer;vertical-align:middle;'
        })
        super().__init__(*args, **kwargs)


def _apply_crop(image_field, crop_json):
    if not crop_json or not image_field:
        return
    try:
        import json
        from PIL import Image
        data = json.loads(crop_json)
        x, y, w, h = int(data['x']), int(data['y']), int(data['w']), int(data['h'])
        if w < 4 or h < 4:
            return
        img = Image.open(image_field.path)
        img = img.crop((x, y, x + w, y + h))
        img.save(image_field.path)
    except Exception:
        pass


class BuyLinkInline(admin.TabularInline):
    model = BuyLink
    extra = 2
    fields = ('store', 'url', 'color', 'icon')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'color':
            field.widget = ColorInput()
        return field


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug', 'preview_image')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'description', 'image', 'color')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'color':
            field.widget = ColorInput()
        return field

    @admin.display(description='Фон')
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{0}" style="height:32px;width:64px;'
                'object-fit:cover;border-radius:4px;">',
                obj.image.url
            )
        return format_html(
            '<span style="display:inline-block;width:40px;height:20px;'
            'border-radius:3px;background:{0};"></span>', obj.color
        )


class AuthorAdminForm(forms.ModelForm):
    # crop_data JSON {x,y,w,h}
    crop_data = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model  = Author
        fields = '__all__'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form   = AuthorAdminForm
    list_display = ('name', 'slug', 'preview_photo')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'bio', 'photo', 'crop_data')

    @admin.display(description='Фото')
    def preview_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{0}" style="height:40px;width:40px;'
                'object-fit:cover;border-radius:50%;">', obj.photo.url
            )
        return '—'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        _apply_crop(obj.photo, form.cleaned_data.get('crop_data', ''))


class BookAdminForm(forms.ModelForm):
    crop_data = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model  = Book
        fields = '__all__'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form   = BookAdminForm
    list_display = ('title', 'year', 'rating', 'preview_cover')
    list_filter  = ('genres',)
    search_fields = ('title', 'authors__name')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('authors', 'genres')
    inlines = [BuyLinkInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'authors', 'genres',
                       'description', 'year', 'rating')
        }),
        ('Обложка', {
            'fields': ('cover', 'crop_data'),
            'description': 'Загрузите обложку (рек. 400×600 px). '
                           'После загрузки выделите нужную область мышью.',
        }),
    )

    @admin.display(description='Обложка')
    def preview_cover(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{0}" style="height:48px;width:32px;'
                'object-fit:cover;border-radius:3px;">', obj.cover.url
            )
        return '—'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        _apply_crop(obj.cover, form.cleaned_data.get('crop_data', ''))

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        if not change and obj.buy_links.count() == 0:
            q = obj.title.replace(' ', '+')
            BuyLink.objects.create(
                book=obj, store='Литрес',
                url=f'https://www.litres.ru/search/?q={q}',
                color='#FF6B35'
            )
            BuyLink.objects.create(
                book=obj, store='Ozon',
                url=f'https://www.ozon.ru/search/?text={q}',
                color='#005bff'
            )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display  = ('user', 'book', 'added_at')
    readonly_fields = ('added_at',)
