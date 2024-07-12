#!/bin/sh

# Update pot
xgettext --keyword=_ --keyword=ngettext:1,2 --language=Python --no-location --sort-output \
    -o ks_includes/locales/ChromaScreen.pot \
    *.py \
    ks_includes/*.py \
    ks_includes/widgets/*.py \
    panels/*.py \
    ks_includes/defaults.conf
# Update po
for FILE in ks_includes/locales/*; do
    if [ -d $FILE ]; then
        echo Processing $FILE
        msgmerge -q $FILE/LC_MESSAGES/ChromaScreen.po \
                 ks_includes/locales/ChromaScreen.pot \
              -o $FILE/LC_MESSAGES/ChromaScreen.po
        # Clean Fuzzy translations
        msgattrib --clear-fuzzy --empty -o $FILE/LC_MESSAGES/ChromaScreen.po $FILE/LC_MESSAGES/ChromaScreen.po
        # Compile mo
        msgfmt -o  $FILE/LC_MESSAGES/ChromaScreen.mo $FILE/LC_MESSAGES/ChromaScreen.po
    fi
done
