document.getElementById("changePasswordForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Ngăn chặn form reload trang

    // Lấy dữ liệu từ form
    const currentPassword = document.getElementById("currentPassword").value;
    const newPassword = document.getElementById("newPassword").value;
    const renewPassword = document.getElementById("renewPassword").value;

    // Kiểm tra dữ liệu đầu vào
    if (!currentPassword || !newPassword || !renewPassword) {
        alert("Please fill in all fields.");
        return;
    }

    if (newPassword !== renewPassword) {
        alert("New passwords do not match.");
        return;
    }

    try {
        const accountAdmin = "admin";
        const response = await fetch(`http://127.0.0.1:5000/update_admin_password`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                account_admin: accountAdmin,
                current_password: currentPassword,
                new_password: newPassword,
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
        } else {
            alert(result.message || "An error occurred.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while updating the password.");
    }
});
