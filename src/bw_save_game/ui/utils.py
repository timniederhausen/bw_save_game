from imgui_bundle import portable_file_dialogs


def ask_for_file_to_open(message, wildcard):
    dlg = portable_file_dialogs.open_file(title=message, filters=wildcard.split("|"))
    while not dlg.ready():
        pass
    res = dlg.result()
    if res:
        return res[0]
    return None


def ask_for_file_to_save(message, wildcard):
    dlg = portable_file_dialogs.save_file(title=message, filters=wildcard.split("|"))
    while not dlg.ready():
        pass
    return dlg.result()


def show_error(message):
    dlg = portable_file_dialogs.message("Error", message, portable_file_dialogs.choice.ok)
    while not dlg.ready():
        pass
