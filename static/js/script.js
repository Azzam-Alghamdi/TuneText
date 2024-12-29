function loading() {
    const playlistName = document.getElementById('playlist_name').value.trim();
    const playlistDescription = document.getElementById('user_description').value.trim();

    if (playlistName && playlistDescription) {
        document.getElementById('loading').style.display = 'block';
    } else {}
}
document.addEventListener("DOMContentLoaded", () => {
    const usernameContainer = document.getElementById("usernameContainer");
    const welcomeMessage = document.getElementById("welcomeMessage");
    const displayUsername = document.getElementById("displayUsername");
    const saveUsernameButton = document.getElementById("saveUsername");

    document.getElementById('playlist_name').value = '';
    document.getElementById('user_description').value = '';

    // Check if username exists in localStorage
    const savedUsername = localStorage.getItem("username");

    if (savedUsername) {
        // If username exists, show welcome message
        displayUsername.textContent = savedUsername;
        welcomeMessage.style.display = "block";
    } else {
        // If no username, show input container
        usernameContainer.style.display = "block";
    }

    saveUsernameButton.addEventListener("click", () => {
        const usernameInput = document.getElementById("username").value.trim();

        if (usernameInput) {
        // Save username in localStorage
        localStorage.setItem("username", usernameInput);

        // Update UI
        displayUsername.textContent = usernameInput;
        usernameContainer.style.display = "none";
        welcomeMessage.style.display = "block";
        } else {
        alert("Please enter a username.");
        }
  });
});