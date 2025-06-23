## Instalation

```bash
uv tool install https://github.com/BogdanVR666/sprava.git
```

## Uninstalation 

```bash
uv tool uninstall strava
```

## Usage 

### Add task

```bash
todo add "Task text"
todo add "Task text" --deadline "2025-06-23"
```

### Done task

```bash
todo done --id 2
```

### Remove task

```bash
todo remove --id 2
```

### Show tasks 

```bash
todo list
todo list --recursive (soon)
```
