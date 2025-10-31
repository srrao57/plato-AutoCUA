# plato-AutoCUA

## 🗂️ Project Structure

```

baserow-setup/
├─ README.md                        ← this file
├─ baserow_info.md                  ← collected metadata & test plan
├─ inputs.yml                       ← repo + env configuration
├─ plato-config.yml                 ← compute + verification spec
├─ base/
│   └─ docker-compose.yml           ← adapted for host networking
├─ scripts/
│   ├─ bootstrap.sh                 ← brings up docker & runs checks
│   └─ health_check.sh              ← HTML/API health verification
├─ tests.yml                        ← deterministic curl-based tests
├─ run_baserow_autosetup.claude.md  ← Claude automation plan (steps 2–7)
└─ AUTORUN_LOG.md                   ← generated log of last run

````

---

## ⚙️ Local Setup

### 1️⃣ Mount local folder into the Plato VM

Keep all files locally (e.g. `~/plato-projects/baserow-setup`)  
and mount them directly into the Plato microVM:

```bash
plato sims ssh sandbox-24 \
  --mount ~/plato-projects/baserow-setup:/home/plato/baserow-setup
````

Now inside the VM:

```bash
cd ~/baserow-setup
ls
```

You should see your full local folder mirrored in the microVM.

---

## 🤖 Claude Setup in the MicroVM

### 1. Mount the Claude binary

Download npm

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Load nvm into shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Install latest LTS Node
nvm install --lts
```

Copy or mount your local Claude CLI binary into the same VM:

```bash
scp -F /Users/vamsi/.plato/ssh_24.conf /opt/homebrew/bin/claude sandbox-24:~/claude
```

Then inside the VM:

```bash
chmod +x ~/claude
mkdir -p ~/.local/bin
mv ~/claude ~/.local/bin/claude
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
claude --version
```

Expected output:

```
2.0.xx (Claude Code)
```

---

### 2. Configure Claude for API-key (headless) mode

Export environment variables once logged into the microVM:

```bash
export CLAUDE_API_KEY=$ANTHROPIC_API_KEY
export CLAUDE_DISABLE_OAUTH=1
export CLAUDE_AUTO_APPROVE=1
export CLAUDE_SKIP_CONFIRM=1
export CLAUDE_MODE=api
```

Then confirm Claude is working:

```bash
claude -p "Hello from API mode"
```

Expected output:

```
Hello! Claude API mode is working correctly.
```

---

## 🧠 Run Claude Automation

Run the complete Baserow automation plan autonomously:

```bash
claude -p "$(cat run_baserow_autosetup.claude.md)"
```

Claude will:

1. Validate `base/docker-compose.yml` and `plato-config.yml`
2. Run `scripts/bootstrap.sh`
3. Execute health checks until passing
4. Log results to `AUTORUN_LOG.md`
5. Snapshot the VM using the Plato SDK

---

## 🧩 Compute Specs

Defined in `plato-config.yml`:

```yaml
compute:
  cpus: 1
  memory_mb: 512
  disk_gb: 8
```

This configuration ensures minimal resource usage compatible with Plato microVMs.

---

## ✅ Deliverables

At completion, the working directory will contain:

```
docker-compose.yml
plato-config.yml
scripts/bootstrap.sh
scripts/health_check.sh
tests.yml
AUTORUN_LOG.md
summary.txt
```

All tests passing and the VM snapshot stored via Plato.

---
