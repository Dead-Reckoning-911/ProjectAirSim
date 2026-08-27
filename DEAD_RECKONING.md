# Dead Reckoning host (this fork)

This is **not** a vanilla IAMAI checkout.

- Org: [Dead-Reckoning-911/ProjectAirSim](https://github.com/Dead-Reckoning-911/ProjectAirSim)
- Branch to use: **`mac-ue57-host`** (org default)
- What it adds: macOS/arm64 Unreal 5.7 host, Apple OpenSSL client auth, Darwin Python
  client, DownCamera streaming for the Airdrone-Reckoning operator feed

Upstream is `iamaisim/ProjectAirSim`. Official PAS is Windows 11 / Ubuntu 22. The Mac
patches live only on `mac-ue57-host`. You do not need upstream `main` to run the intercept
demo on this machine.

## Demo

Unreal Blocks `-game` + Airdrone dashboard. See
[`Airdrone-Reckoning/docs/DEMO_UNREAL.md`](https://github.com/Dead-Reckoning-911/Airdrone-Reckoning/blob/main/docs/DEMO_UNREAL.md).

```bash
git clone https://github.com/Dead-Reckoning-911/ProjectAirSim.git
cd ProjectAirSim
git checkout mac-ue57-host   # no-op if this is already the default
```

Do not clone `microsoft/AirSim` for this work. Do not vendor this tree into `Dead_Reckoning`.
