# debug_i18n.py
import os
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAdminTemplate.settings')

django.setup()

from django.conf import settings
from django.utils import translation

print("=== ДИАГНОСТИКА ПЕРЕВОДОВ ===")
print(f"1. BASE_DIR: {BASE_DIR}")
print(f"2. LOCALE_PATHS: {settings.LOCALE_PATHS}")
print(f"3. LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
print(f"4. USE_I18N: {settings.USE_I18N}")

# Проверка файлов
locale_path = BASE_DIR / 'locale' / 'ru' / 'LC_MESSAGES'
print(f"\n5. Проверка папки: {locale_path}")
if locale_path.exists():
    for file in locale_path.iterdir():
        print(f"   - {file.name}: {file.stat().st_size} байт")
else:
    print("   ❌ Папка не существует!")

# Тест перевода
print("\n6. Тест перевода:")
translation.activate('ru')
from django.utils.translation import gettext

test_words = ['Product', 'Save', 'Delete', 'Name']
for word in test_words:
    translated = gettext(word)
    status = "✓" if word != translated else "❌"
    print(f"   {status} '{word}' -> '{translated}'")

# Проверка загрузки переводов
print("\n7. Проверка загрузки переводов:")
from django.utils.translation import trans_real
try:
    catalog = trans_real._translations.get('ru', {}).get('django')
    if catalog:
        print(f"   ✓ Переводы загружены")
        print(f"   Количество сообщений: {len(catalog._catalog)}")
    else:
        print("   ❌ Переводы не загружены")
except:
    print("   ❌ Ошибка при проверке переводов")