/**
 * Class that handles alert windows shown to the user.
 */
class AlertUser {
    /**
     * @param {string} parentDiv - jQuery designation of the parent div
     */
    constructor(parentDiv)
    {
        this.parentDiv = $(parentDiv);
        this.parentDiv.addClass("alertmessages");
        this.hide();
    }

    /**
     * Hides the AlertUser and its parent div.
     */
    hide()
    {
        var thisAlertUser = this;
        this.parentDiv.empty();
        $('<button class="ui small compact secondary button closebtn">\
        &times;</button>').appendTo(this.parentDiv);
        this.parentDiv.find('.closebtn')
            .on('click', function() {
                thisAlertUser.hide();
            });
        this.parentDiv.hide();
    }

    /**
     * Shows a message to the user.
     *
     * @param {string} msg - Message to display
     * @param {string} title - Title of the message
     * @param {string} type - Type of the alert ('info', 'success', 'warning' or 'error')
     */
    showMessage(msg, title, type)
    {
        $('<div class="ui '+type+' message">\
        <div class="header">'+title+'</div>\
      <p>'+msg+'</p></div>').appendTo(this.parentDiv);
        this.parentDiv.show();
    }

    /**
     * Shows an informative message.
     *
     * @param {string} msg - Message to display
     * @param {string} title - Title of the message (default: 'Info')
     */
    showInfo(msg, title='Info')
    {
        this.showMessage(msg, title, "info");
    }

    /**
     * Shows a message notifying a success.
     *
     * @param {string} msg - Message to display
     * @param {string} title - Title of the message (default: 'Success')
     */
    showSuccess(msg, title='Success')
    {
        this.showMessage(msg, title, "success");
    }

    /**
     * Shows a warning message.
     *
     * @param {string} msg - Message to display
     * @param {string} title - Title of the message (default: 'Warning')
     */
    showWarning(msg, title='Warning')
    {
        this.showMessage(msg, title, "warning");
    }

    /**
     * Shows a message notifying an error.
     *
     * @param {string} msg - Message to display
     * @param {string} title - Title of the message (default: 'Error')
     */
    showError(msg, title='Error')
    {
        this.showMessage(msg, title, "error");
    }
}
