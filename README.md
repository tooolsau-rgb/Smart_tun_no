# SmartClaw Android + OpenClaw VPS Bridge

## What is implemented
- Kivy Android chat UI, Gateway/Telegram status, OpenClaw nodes list/status.
- Windows local-only HTTP bridge with bearer authentication, no arbitrary shell commands.
- GitHub Actions debug APK build. No Ubuntu installation on your Windows VPS.
- No secrets are included in the APK or repository.

## What is NOT implemented
- Native OpenClaw Android node pairing/camera/screen/location: requires official OpenClaw Android client and supported node protocol. Use the official Android app separately for pairing.
- General remote PowerShell execution: intentionally excluded for safety.
- Telegram bot itself is not embedded; the bridge uses the existing OpenClaw agent on the VPS.

## 1. On Windows VPS (PowerShell)
Install Python 3.11+ if needed. In a PowerShell session, from the `vps` folder:

```powershell
$env:SMARTCLAW_BRIDGE_TOKEN = ([guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N'))
$env:SMARTCLAW_BRIDGE_TOKEN | Set-Clipboard
python .\bridge.py
```

Keep this terminal open for initial testing. **Store the generated token securely; do not paste it into chats, logs or GitHub.** To run as a background service later, configure a restricted Windows Scheduled Task with a protected environment variable. Avoid placing the token in a publicly readable script.

OpenClaw CLI must be on PATH for the Windows account running the bridge. Verify `openclaw agent --help`; on this OpenClaw version, the bridge calls `openclaw agent --agent main --message <text>`. Some versions may require additional arguments or JSON parsing; test locally first.

## 2. Expose bridge via Tailscale Serve, not Funnel
The existing Tailscale Serve proxy on port 18789 is for the OpenClaw Gateway. **Do not overwrite it.** The bridge listens on `127.0.0.1:18890` and must use its own HTTPS endpoint. Check your installed Tailscale CLI version and `tailscale serve --help` for configuring an additional HTTPS port/handler (e.g. HTTPS 8443 -> local 18890). Do not run `tailscale serve --bg 18890` without checking: it could replace the existing 443 route.

Verify the new URL from an Android phone signed into the same tailnet. Use a valid Tailscale HTTPS hostname and the matching port. Never expose bridge to the public Internet or use Tailscale Funnel.

## 3. Android app
Enter the **HTTPS URL of the bridge** (not the existing Gateway URL unless you explicitly configured a separate bridge path), and the `SMARTCLAW_BRIDGE_TOKEN` you generated. The token is kept in app memory only; it is not saved to disk. Each app restart requires re-entry. This is deliberate for a simple secure prototype.

## 4. Build APK with GitHub Actions
Create a private GitHub repository. Upload all files preserving folders, then Actions -> Build SmartClaw APK -> Run workflow. After the build completes, download the `SmartClaw-debug-apk` artifact. Enable install from trusted sources on Android for local testing. Debug APK is for testing, not Play Store release.

Buildozer/Android SDK versions can change; if the first CI run fails, review the Actions logs and pin versions accordingly. The provided workflow is a starting build pipeline, not a pre-built or verified APK.

## 5. Security
- Gateway and Telegram credentials are never used by the Android client.
- Keep bridge bound to localhost and exposed only over authenticated Tailscale HTTPS.
- The bridge token is separate from the OpenClaw Gateway token.
- Chat messages are forwarded to your existing OpenClaw agent, so only trusted users should receive bridge credentials. OpenClaw agent tools may have powerful permissions; restrict the agent's tool policy appropriately.
- If a token is disclosed, rotate it and restart only the bridge.
- API usage still depends on OpenClaw provider quota; this bridge does not bypass cooldown or subscription limits.
