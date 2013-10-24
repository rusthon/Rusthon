ON_GOING = 0
DONE = 1

class TodoItem:

    def __init__(self, title, list):
        self.title = title
        self.list = list
        self.status = ON_GOING
        self.ui = jQuery('<li></li>')

    def render(self):
        self.ui.empty()
        self.ui.append(self.title + " ")
        if self.status == ON_GOING:
            done = jQuery("<span>[done?]<span>")
            done.click(self._on_done)
            self.ui.append(done)
        return self.ui

    def _on_done(self, event):
        self.status = DONE
        self.render()

