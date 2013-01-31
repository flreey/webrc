var createLoginBox= function(){
    if ('undefined' === typeof chatWindowId){
        chrome.windows.create(
            {
                'url': chrome.extension.getURL("popup.html")
                ,'width': 280
                ,'height': 400
                ,'left': window.screen.width - 300
                ,'top': window.screen.height - 390
                ,'type': 'panel'
                ,'focused': true
            },

            function(chatWindow){
                chatWindow.alwaysOnTop = true;
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

chrome.browserAction.onClicked.addListener(createLoginBox);
