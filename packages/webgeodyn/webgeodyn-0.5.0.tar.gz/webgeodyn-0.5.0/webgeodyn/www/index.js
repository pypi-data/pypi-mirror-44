$(document).ready(function() {
    //Get close uuid
    var closeUUID;
    $.ajax("close", {
        type: 'GET',
        dataType: "json",
    }).done(function(response) {
        closeUUID = response.closeUUID
        console.log("GOT CLOSE UUID",response,closeUUID)
    }).fail(function(xhr, status, error) {
        console.log("Server is not closable by client. ( GET /close",xhr.status,error,")")
    });

    //Send close when user close tab (allows closing of server when in interactive mode)
    var closed = false;
    window.onbeforeunload = function(){
        if (!closed) {
            console.log("Sending close with UUID", closeUUID);
            closed = true;
            $.ajax("close", {
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify({"closeUUID":closeUUID}),
            }).always(function(){
                console.log("Closed sent");
            });
        }
    }

    window.mc = new MainController();
});
