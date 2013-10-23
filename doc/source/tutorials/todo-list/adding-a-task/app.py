submit = jQuery("input[type='submit']")


def on_add():
    input = jQuery("input[type='text']")
    task = input.val()  # fetch the value of the input
    if task:
        # if it's not empty add it to the list
        tasks = jQuery('#tasks')
        tasks.append("<li>" + task + "</li>")
        # empty the input field
        input.val('')


submit.click(on_add)
