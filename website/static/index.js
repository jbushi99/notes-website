function deleteNote(noteId){
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId })
    }).then((_res)=>{
        window.location.href="/";
    });
}

function deleteMessage(messageId){
    fetch("/delete-message", {
        method: "POST",
        body: JSON.stringify({ messageId: messageId })
    }).then((_res)=>{
        window.location.href="/inbox";
    });
}

function updateStatus(status, noteId){
    fetch("/update-note-status", {
        method: "POST",
        body: JSON.stringify({ status: status, noteId: noteId })
    }).then((_res)=>{
        window.location.href="/";
    });
}

function searchUser(userinput){
    window.location.href="/others/"+ userinput
}

function addFriend(friendID, friendUsername){
    fetch("/add-friend", {
        method: "POST",
        body: JSON.stringify({ user_id2: friendID})
    }).then((_res)=>{
        window.location.href="/others/" + friendUsername;
    });
}

function deleteFriend(friendID, friendUsername){
    fetch("/delete-friend", {
        method: "POST",
        body: JSON.stringify({ user_id2: friendID })
    }).then((_res)=>{
        window.location.href="/others/" + friendUsername;
    });
}

function changeFollowStatus(friendID, friendUsername, followButtonText){
    //var myButton = document.getElementById("followbutton");
    //alert(followButtonText);
    console.log(followButtonText);
    if (followButtonText === "FOLLOW"){
       addFriend(friendID, friendUsername);
    } 
    else{
        deleteFriend(friendID, friendUsername);
    }
}