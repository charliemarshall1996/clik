document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll("input[name='interests']");
    const submitButton = document.querySelector("button[type='submit']");
    const maxSelections = 5;

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const selectedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
            
            // Disable unchecked checkboxes if limit reached
            if (selectedCount >= maxSelections) {
                checkboxes.forEach(cb => {
                    if (!cb.checked) {
                        cb.disabled = true;
                    }
                });
            } else {
                // Re-enable checkboxes if under limit
                checkboxes.forEach(cb => cb.disabled = false);
            }
            
            // Optional: Disable submit button if over limit
            submitButton.disabled = selectedCount > maxSelections;
        });
    });
});
