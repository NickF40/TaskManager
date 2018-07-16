def languageuser (code):
    if code == 'ru-RU':
        from  code.language.russian import *
    if code == 'en-EN':
        from code.language.english import *
    pass
