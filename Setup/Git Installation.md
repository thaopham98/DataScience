# Git Installation Documentation

## Installation Details
- **Version Installed:** Git 2.47.1.2
- **Installation Path:** `C:\Program Files\Git`

![Select Destination Location](images/Setup/Git Installation/Step 1 - Select Destination Location.png)

- **Installation Date:** [Insert Date Here]

---

## Selected Components
1. **Additional Icon on the Desktop:**
   - Enabled (for quick access to Git).

2. **Windows Explorer Integration:**
   - `Open Git Bash here`
   - `Open Git GUI here`

3. **Git LFS (Large File Support):**
   - Enabled (for managing large files).

4. **File Associations:**
   - Associate `.git*` configuration files with the default text editor (VSCode).
   - Associate `.sh` files to be run with Bash.

5. **Scalar (Git Add-on):**
   - Enabled (for managing large-scale repositories).

---

## Configuration Settings
1. **Default Editor:**
   - **Visual Studio Code** (set as Git’s default editor for commit messages and other tasks).

2. **Initial Branch Name:**
   - **Let Git decide** (default branch name will be `main`).

3. **PATH Environment:**
   - **Git from the command line and also from 3rd-party software** (Git added to system PATH).

4. **SSH Executable:**
   - **Use bundled OpenSSH** (default).

5. **HTTPS Transport Backend:**
   - **Use the OpenSSL library** (default).

6. **Line Ending Conversions:**
   - **Checkout Windows-style, commit Unix-style line endings** (recommended for cross-platform compatibility).

7. **Terminal Emulator:**
   - **Use MinTTY** (default terminal for Git Bash).

8. **Default Behavior of `git pull`:**
   - **Fast-forward or merge** (default).

9. **Credential Helper:**
   - **Git Credential Manager** (for securely managing GitHub credentials).

10. **Extra Options:**
    - **Enable file system caching** (improves performance for large repositories).

---

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
     git config --global user.name
     git config --global user.email
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