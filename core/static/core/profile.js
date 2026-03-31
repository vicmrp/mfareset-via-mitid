document.addEventListener("DOMContentLoaded", function () {
    const resetBtn = document.getElementById("reset-mfa-btn");
    const modalElement = document.getElementById("reset-mfa-modal");
    const confirmBtn = document.getElementById("confirm-reset-btn");
    const statusBox = document.getElementById("reset-status");

    const modal = new bootstrap.Modal(modalElement);

    const csrfTokenInput = document.querySelector("input[name=csrfmiddlewaretoken]");
    const csrfToken = csrfTokenInput ? csrfTokenInput.value : "";

    function showStatus(message, type = "success") {
        statusBox.textContent = message;
        statusBox.className = "alert mb-4";

        if (type === "success") {
            statusBox.classList.add("alert-success");
        } else {
            statusBox.classList.add("alert-danger");
        }

        statusBox.classList.remove("d-none");

        setTimeout(() => {
            statusBox.classList.add("d-none");
        }, 4000);
    }

    resetBtn.addEventListener("click", function () {
        modal.show();
    });

    confirmBtn.addEventListener("click", async function () {
        confirmBtn.disabled = true;
        confirmBtn.textContent = "Resetting...";

        try {
            const response = await fetch("/reset-mfa/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/json"
                }
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Something went wrong.");
            }

            modal.hide();
            showStatus(data.message || "MFA reset completed.", "success");
        } catch (error) {
            showStatus(error.message || "Reset failed.", "error");
        } finally {
            confirmBtn.disabled = false;
            confirmBtn.textContent = "Confirm";
        }
    });
});