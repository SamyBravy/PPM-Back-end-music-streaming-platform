document.addEventListener('DOMContentLoaded', function () {
    const iconPicker = document.getElementById('id_profile_icon_picker');
    const iconInputs = document.querySelectorAll('input[name="profile_icon"]');

    const updateSelected = function () {
        iconInputs.forEach(function (input) {
            const label = input.closest('label.icon-picker-option');
            if (label) {
                label.classList.toggle('selected', input.checked);
            }
        });
    };

    if (iconPicker) {
        iconPicker.addEventListener('click', function (event) {
            const label = event.target.closest('label.icon-picker-option');
            if (!label) {
                return;
            }

            const input = label.querySelector('input[type="radio"]');
            if (input) {
                input.checked = true;
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    }

    iconInputs.forEach(function (input) {
        input.addEventListener('change', updateSelected);
    });

    updateSelected();
});
