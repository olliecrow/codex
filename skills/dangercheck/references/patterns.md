# Red-Flag Scan Patterns

Use ripgrep (`rg`) with `--hidden` and add `--no-ignore` if you need to include dotfiles and normally ignored files. Exclude large vendored dirs if needed.

Example baseline:
- `rg -n --hidden -g '!.git/**' -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' <pattern>`

## Download + execute

- `rg -n --hidden -g '!.git/**' '(curl|wget|Invoke-WebRequest|iwr|bitsadmin|certutil).*(sh|bash|cmd|ps1|python|node)'`
- `rg -n --hidden -g '!.git/**' '(curl|wget).*(\|\s*(sh|bash|python|node))'`
- `rg -n --hidden -g '!.git/**' '(git clone|svn checkout|hg clone)\s+https?://'`

## Dynamic execution

- `rg -n --hidden -g '!.git/**' '(eval\(|exec\(|new Function|Function\(|setTimeout\(|setInterval\()'`
- `rg -n --hidden -g '!.git/**' '(child_process|spawn\(|execFile\(|fork\()'`
- `rg -n --hidden -g '!.git/**' '(os\.system|subprocess\.|popen\()'`
- `rg -n --hidden -g '!.git/**' '(Runtime\.getRuntime\(\)\.exec|ProcessBuilder)'`

## Obfuscation / encoded payloads

- `rg -n --hidden -g '!.git/**' '(base64|atob|btoa|fromCharCode|String\.fromCharCode)'`
- `rg -n --hidden -g '!.git/**' '(xxd -r|openssl enc|gzip -d|gunzip|tar -x)'`
- `rg -n --hidden -g '!.git/**' '(Invoke-Expression|iex|powershell -enc|\b-EncodedCommand\b)'`

## Privilege escalation and persistence

- `rg -n --hidden -g '!.git/**' '(sudo|pkexec|runas|setcap|chmod \+s|chown root)'`
- `rg -n --hidden -g '!.git/**' '(crontab|systemctl|launchctl|schtasks|reg add|update-rc\.d)'`
- `rg -n --hidden -g '!.git/**' '(/etc/|/Library/LaunchAgents|/Library/LaunchDaemons|~/.ssh|authorized_keys)'`

## Data access / exfiltration

- `rg -n --hidden -g '!.git/**' '(AWS_|GCP_|AZURE_|GOOGLE_|SSH_|TOKEN|SECRET|KEYCHAIN|KEYRING)'`
- `rg -n --hidden -g '!.git/**' '(curl|wget|requests\.post|axios\.post|fetch\()'`
- `rg -n --hidden -g '!.git/**' '(webhook|pastebin|ngrok|tunnel|exfil|upload)'`

## Destructive operations

- `rg -n --hidden -g '!.git/**' '(rm -rf /|del /f /s|format\s+[A-Z]:|mkfs\.|dd if=/dev/zero)'`

## Crypto-mining indicators

- `rg -n --hidden -g '!.git/**' '(xmrig|minerd|stratum|cryptonight|cpu\-mine)'`

## Supply-chain hooks

- `rg -n --hidden -g '!.git/**' '(postinstall|preinstall|prepare|install|prepack|postpack|prepublish)' package.json`
- `rg -n --hidden -g '!.git/**' '(git\+https?|https?://).*#' requirements*.txt`
- `rg -n --hidden -g '!.git/**' '(extra-index-url|trusted-host|--index-url|--find-links)' requirements*.txt`
- `rg -n --hidden -g '!.git/**' 'url\s*=\s*"?https?://' pyproject.toml setup.cfg`
- `rg -n --hidden -g '!.git/**' 'build\s*=\s*"build\.rs"' Cargo.toml`

## OS-specific persistence

- macOS: `rg -n --hidden -g '!.git/**' '(launchd|launchctl|defaults write|plist)'`
- Windows: `rg -n --hidden -g '!.git/**' '(schtasks|reg add|powershell|cmd /c)'`
