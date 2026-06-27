(function () {
    const audioInput = document.getElementById('id_audio_file');
    const durationInput = document.getElementById('id_duration');

    window.unlockDuration = function() {
        if (durationInput) {
            durationInput.readOnly = false;
            durationInput.style.backgroundColor = '';
            durationInput.style.pointerEvents = 'auto';
            
            // hide help text if exists
            const helpText = document.getElementById('hint_id_duration');
            if (helpText) {
                helpText.style.display = 'none';
            }
        }
    };

    if (audioInput && durationInput) {
        audioInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                // Leggiamo la durata se è un file valido
                const objectUrl = URL.createObjectURL(file);
                const audio = new Audio(objectUrl);

                const updateDuration = function (dur) {
                    if (isFinite(dur)) {
                        const hours = Math.floor(dur / 3600);
                        const minutes = Math.floor((dur % 3600) / 60);
                        const seconds = Math.floor(dur % 60);

                        let formattedDuration = '';
                        if (hours > 0) formattedDuration += hours.toString().padStart(2, '0') + ':';
                        formattedDuration += minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');

                        durationInput.value = formattedDuration;
                        durationInput.readOnly = true;
                        durationInput.style.backgroundColor = '#e9ecef';
                        durationInput.style.pointerEvents = 'none';
                    }
                };

                audio.addEventListener('loadedmetadata', function () {
                    if (audio.duration === Infinity) {
                        // Chrome bug workaround per blob audio
                        audio.currentTime = Number.MAX_SAFE_INTEGER;
                        audio.ontimeupdate = function() {
                            audio.ontimeupdate = null;
                            updateDuration(audio.duration);
                            audio.currentTime = 0;
                            URL.revokeObjectURL(objectUrl);
                        };
                    } else {
                        updateDuration(audio.duration);
                        URL.revokeObjectURL(objectUrl);
                    }
                });

                audio.addEventListener('error', function () {
                    // Se non riesce a leggerlo (file non valido), sblocca
                    durationInput.readOnly = false;
                    durationInput.style.backgroundColor = '';
                    durationInput.style.pointerEvents = 'auto';
                });

            } else {
                durationInput.readOnly = false;
                durationInput.style.backgroundColor = '';
                durationInput.style.pointerEvents = 'auto';
            }
        });
    }
})();
