class TodoList:

    def __init__(self, id):
        self.ui = JSObject()
        # Retrieve the useful elements of this widget
        self.ui.root = jQuery(id)
        self.ui.list = jQuery('ul', self.ui.root)
        self.ui.input = jQuery("input[type='text']", self.ui.root)
        self.ui.submit = jQuery("input[type='submit']", self.ui.root)
        # hook click event (jQuery call)
        self.ui.submit.click(self._on_submit)  

        # task will be stored here
        self.items = list()

    def _on_submit(self, event):
        title = self.ui.input.val()  # retrieve task description (jQuery call)
        if title:
            item = TodoItem(title, self)  # create task from task description
            self.items.append(item)
            html = item.render()  # render the task
            self.ui.list.append(html)  # add the html to the ul (jQuery call)
            self.ui.input.val('')  # empty the input field (jQuery call)


class TodoItem:

    def __init__(self, title, list):
        self.title = title
        self.list = list

    def render(self):
        return "<li>" + self.title + "</li>"
