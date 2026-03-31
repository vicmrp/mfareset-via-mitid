document.addEventListener("DOMContentLoaded", function () {
    const resetBtn = document.getElementById("reset-mfa-btn");
    const modal = document.getElementById("reset-mfa-modal");
    const cancelBtn = document.getElementById("cancel-reset-btn");
    const confirmBtn = document.getElementById("confirm-reset-btn");
    const modalBox = modal.querySelector(".modal-box");
    const statusBox = document.getElementById("reset-status");

    const csrfTokenInput = document.querySelector("input[name=csrfmiddlewaretoken]");
    const csrfToken = csrfTokenInput ? csrfTokenInput.value : "";

    function openModal() {
        modal.classList.remove("hidden");
    }

    function closeModal() {
        modal.classList.add("hidden");
    }

    function showStatus(message, type = "success") {
        statusBox.textContent = message;
        statusBox.className = `status-toast ${type}`;
        statusBox.classList.remove("hidden");

        setTimeout(() => {
            statusBox.classList.add("hidden");
        }, 4000);
    }

    resetBtn.addEventListener("click", function (event) {
        event.preventDefault();
        openModal();
    });

    cancelBtn.addEventListener("click", function () {
        closeModal();
    });

    modal.addEventListener("click", function (event) {
        if (!modalBox.contains(event.target)) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && !modal.classList.contains("hidden")) {
            closeModal();
        }
    });

    // Initiates mfa-reset-server-request
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

            closeModal();
            showStatus(data.message || "MFA reset completed.", "success");
        } catch (error) {
            showStatus(error.message || "Reset failed.", "error");
        } finally {
            confirmBtn.disabled = false;
            confirmBtn.textContent = "Confirm";
        }
    });
});