# Git Installation Documentation

## Installation Details
- **Version Installed:** Git 2.47.1.2
- **Installation Path:** `C:\Program Files\Git`
- **Installation Date:** February 7, 2025

---
### Step 1: Select Destination Location
![Select Destination Location](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%201%20-%20Select%20Destination%20Location.png)

### Step 2: Select Start Menu Folder
![Select Start Menu Folder](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%202%20-%20Select%20Start%20Menu%20Folder.png)

### Step 3: Select Components
![Select Components](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%203%20-%20Select%20Components.png)

1. **Windows Explorer Integration:**
   - `Open Git Bash here`
   - `Open Git GUI here`

2. **Git LFS (Large File Support):**
   - Enabled (for managing large files).

3. **File Associations:**
   - Associate `.git*` configuration files with the default text editor (VSCode).
   - Associate `.sh` files to be run with Bash.

4. **Scalar (Git Add-on):**
   - Enabled (for managing large-scale repositories).

---
### Step 4: Choosing the default editor used by Git
![Choosing the default editor used by Git](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%204%20-%20Choosing%20the%20default%20editor%20used%20by%20Git.png)

### Step 5: Adjusting the name of the initial branch in new repositories
![Adjusting the name of the initial branch in new repositories](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%205%20-%20Adijusting%20the%20name%20of%20the%20initial%20branch%20in%20new%20repositories.png)

### Step 6: Adjusting your PATH environment
![Adjusting your PATH environment](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%206%20-%20Adjusting%20your%20PATH%20environment.png)

### Step 7: Choosing the SSH executable
![Choosing the SSH executable](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%207%20-%20Choosing%20the%20SSH%20executable.png)

### Step 8: Choosing HTTPS transport backend
![Choosing HTTPS transport backend](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%208%20-%20Choosing%20HTTPS%20transport%20backend.png)

### Step 9: Configuring the line ending conversions
![Configuring the line ending conversions](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%209%20-%20Configuring%20the%20line%20ending%20conversions.png)

### Step 10: Configuring the terminal emulator to use with Git Bash
![Configuring the terminal emulator to use with Git Bash](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%2010%20-%20Configuring%20the%20terminal%20emulator%20to%20use%20with%20Git%20Bash.png)

### Step 11: Choose the default behavior of `git pull`
![Choose the default behavior of `git pull`](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%2011%20-%20Choose%20the%20default%20behavior%20of%20%60git%20pull%60.png)

### Step 12: Choose a credential helper
![Choose a credential helper](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%2012%20-%20Choose%20a%20credential%20helper.png)

### Step 13: Configuring extra options
![Configuring extra options](https://github.com/thaopham98/DataScience/blob/main/images/Setup/Git%20Installation/Step%2013%20-%20Configuring%20extra%20options.png)

## Post-Installation Verification
1. **Verify Git Installation:**
   - Open Command Prompt and run:
     ```bash
     git --version
     ```
   - Expected output: `git version 2.47.1.2`

2. **Verify Git Configuration:**
   - Run the following commands to check your Git configuration:
     ```bash
     git config --global user.name "user_name_here"
     git config --global user.email "user_email_address_here@email.com"
     ```
   - Ensure these match your GitHub credentials.

3. **Verify Default Editor:**
   - Run the following command to check the default editor:
     ```bash
     git config --global core.editor
     ```
   - Expected output: `code --wait` (for Visual Studio Code).

---

## Integration with GitHub Desktop
1. **Install GitHub Desktop:**
   - Download and install GitHub Desktop from [GitHub Desktop](https://desktop.github.com/).

2. **Configure External Editor in GitHub Desktop:**
   - Open GitHub Desktop.
   - Go to **File > Options** (Windows) or **GitHub Desktop > Preferences** (macOS).
   - Under the **Integrations** tab, set the **External Editor** to **Visual Studio Code**.

3. **Test Integration:**
   - Open a repository in GitHub Desktop.
   - Right-click on a file and select **Open in Visual Studio Code** to verify the integration.

---

## Troubleshooting
1. **Git Not Recognized in Command Prompt:**
   - Ensure Git was added to the system PATH during installation.
   - If not, manually add `C:\Program Files\Git\cmd` to the PATH environment variable.

2. **Commit Messages Not Opening in VSCode:**
   - Verify the default editor is set to VSCode:
     ```bash
     git config --global core.editor "code --wait"
     ```

3. **GitHub Desktop Not Opening Files in VSCode:**
   - Ensure VSCode is set as the external editor in GitHub Desktop’s settings.

---

## Additional Notes
- **Git Credential Manager:** This will securely store your GitHub credentials, so you don’t need to enter them repeatedly.
- **Scalar:** This is optional but useful if you work with very large repositories.
- **Git LFS:** Use this if you work with large files (e.g., images, videos, datasets).

---

## Next Steps
1. **Install GitHub Desktop** (if you haven’t already).
2. **Clone a Repository:**
   - Use Git or GitHub Desktop to clone a repository to your local machine.
3. **Start Using Git:**
   - Use Git commands or GitHub Desktop to manage your repositories.
