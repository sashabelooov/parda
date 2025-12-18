from django.apps import AppConfig


class PardaConfig(AppConfig):
    name = 'parda'

    def ready(self):
        # Ensure jazzmin paginator returns SafeText in production without relying on
        # local venv edits. This is a defensive monkeypatch to avoid template errors
        # if the upstream package has the format_html misuse.
        try:
            import importlib
            from django.utils.safestring import mark_safe

            m = importlib.import_module('jazzmin.templatetags.jazzmin')
            orig = getattr(m, 'jazzmin_paginator_number', None)

            if orig is not None:
                def wrapped(change_list, i):
                    out = orig(change_list, i)
                    # If the original returned a str (not SafeText), mark safe
                    if isinstance(out, str):
                        return mark_safe(out)
                    return out

                m.jazzmin_paginator_number = wrapped
        except Exception:
            # Never raise from ready(); just fall back to the original behavior
            pass
