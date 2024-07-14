// Ensure ClipboardJS is available and initialize it
document.addEventListener("DOMContentLoaded", function() {
    if (typeof ClipboardJS !== "undefined") {
        var clipboard = new ClipboardJS('#copy-button');
        
        clipboard.on('success', function(e) {
            // Show the copied message
            var copiedMessage = document.getElementById('copied-message');
            copiedMessage.style.display = 'inline';
            
            // Hide the message after 2 seconds
            setTimeout(function() {
                copiedMessage.style.display = 'none';
            }, 2000);
            
            e.clearSelection();
        });
        
        clipboard.on('error', function(e) {
            console.error('Failed to copy:', e);
        });
    } else {
        console.error("ClipboardJS is not loaded.");
    }
});