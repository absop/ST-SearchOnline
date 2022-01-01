import webbrowser
import sublime
import sublime_plugin

try:
    from dctxmenu import menu
except:
    sublime.error_message(
        f'The plugin `dctxmenu` is not installed, {__package__} stoped')
    raise


class SerachOnlineMenuCreater(menu.MenuCreater):
    def context_menu(self, event):
        if len(self.platforms) > 0:
            platforms = sorted(self.platforms)
            if content := self.get_selected(event):
                if len(platforms) == 1:
                    platform = platforms[0]
                    url = self.platforms[platform]
                    return self.item(
                        "Search With " + platform,
                        # Command defined in dctxmenu
                        'open_file_with_default_application',
                        {"file": url % content }
                    )
                else:
                    return self.folded_item(
                        self.caption,
                        [ self.item(
                            platform,
                            'open_file_with_default_application',
                            {"file": url % content}
                            )
                         for platform, url in self.platforms.items()
                        ]
                    )
        return None

    def get_selected(self, event):
        view = self.view
        pt = view.window_to_text((event["x"], event["y"]))
        selected = view.sel()
        if view.has_non_empty_selection_region():
            selection = selected[0]
            if not selection.empty() and selection.contains(pt):
                content = view.substr(selected[0]).strip()
                if content:
                    return content
        return None

    @classmethod
    def init(cls):
        cls.caption = settings.get('caption', 'Search Online')
        cls.platforms = settings.get('platforms', {})


def reload_settings():
    global settings
    settings = sublime.load_settings('SearchOnline.sublime-settings')
    settings.add_on_change('caption', SerachOnlineMenuCreater.init)
    SerachOnlineMenuCreater.init()


def plugin_loaded():
    sublime.set_timeout_async(reload_settings)
    menu.register(__name__, SerachOnlineMenuCreater)


def plugin_unloaded():
    settings.clear_on_change('caption')
    menu.remove(__name__)
