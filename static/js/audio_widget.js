if (typeof handleAudioSelection === 'undefined') {
    function handleAudioSelection(input, name, checkboxId) {
        if(input.files.length > 0) { 
            document.getElementById('current_' + name + '_text').innerText = input.files[0].name; 
            document.getElementById('current_' + name).classList.add('text-success');
            
            input.style.display = 'none';
            document.getElementById('loaded_state_' + name).style.display = 'block';
            
            if(checkboxId) {
                const checkbox = document.getElementById(checkboxId);
                if(checkbox) checkbox.checked = false;
            }
        }
    }

    function removeAudio(name, checkboxId, inputId) {
        if(checkboxId) {
            const checkbox = document.getElementById(checkboxId);
            if(checkbox) checkbox.checked = true;
        }
        
        document.getElementById('loaded_state_' + name).style.display = 'none';
        const input = document.getElementById(inputId);
        if(input) {
            input.value = '';
            input.style.display = 'block';
        }
        
        if(typeof window.unlockDuration === 'function') window.unlockDuration();
    }
}
