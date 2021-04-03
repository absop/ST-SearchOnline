import webbrowser
import sublime
import sublime_plugin

import dctxmenu


user_settings = 'SearchOnline.sublime-settings'

def plugin_loaded():
    def load_user_settings():
        SearchOnlineCommand.caption = settings.get('caption', 'Search Online')
        SearchOnlineCommand.platforms = settings.get('platforms', {})

    settings = sublime.load_settings(user_settings)
    settings.clear_on_change('caption')
    settings.add_on_change('caption', load_user_settings)

    load_user_settings()

    sublime.set_timeout(
        lambda: dctxmenu.register(__package__,
            SearchOnlineCommand.make_menu),
        500
    )

def plugin_unloaded():
    dctxmenu.deregister(__package__)


class SearchOnlineCommand(sublime_plugin.WindowCommand):
    caption = 'Search Online'
    comamnd = 'search_online'
    platforms = {}

    @classmethod
    def get_selected(cls, view, event):
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
    def make_menu(cls, view, event):
        platforms = sorted(cls.platforms)
        if len(platforms) > 0:
            content = cls.get_selected(view, event)
            if content is not None:
                cls.content = content
                if len(platforms) == 1:
                    return dctxmenu.item("Search With " + platforms[0],
                        cls.comamnd, {"platform": platforms[0]}
                    )
                else:
                    return dctxmenu.fold_items(cls.caption,
                        [ dctxmenu.item(p, cls.comamnd, {"platform": p})
                          for p in platforms
                        ]
                    )
        return None

    def run(self, platform):
        api = self.platforms[platform]
        webbrowser.open_new_tab(api % self.content)
