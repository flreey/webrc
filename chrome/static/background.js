var chatBox = function(){
    if ('undefined' === typeof chatWindowId){
        chrome.windows.create(
            {
                'url': chrome.extension.getURL("index.html")
                ,'width': 280
                ,'height': 400
                ,'left': window.screen.width - 300
                ,'top': window.screen.height - 420
                ,'type': 'panel'
                ,'focused': true
            },

            function(chatWindow){
                chatWindowId = chatWindow.id;

                chrome.windows.onRemoved.addListener(function(window){
                    if (window === chatWindowId){
                        delete chatWindowId;
                    }

                })
            }
        );
    }
}


chrome.browserAction.onClicked.addListener(chatBox);
