const passwordInput = document.getElementById("password");
const passwordToggle = document.getElementById("passwordToggle");

passwordToggle?.addEventListener("click", () => {
    const isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "text" : "password";
    passwordToggle.setAttribute("aria-label", isPassword ? "Sembunyikan password" : "Tampilkan password");
    const icon = passwordToggle.querySelector("i");
    if (icon) {
        icon.className = isPassword ? "bi bi-eye-slash" : "bi bi-eye";
    }
});
