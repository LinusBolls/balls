import json

def haveSameKeys(objects):
  for i in range(1, len(objects)):
    if (sorted(objects[i].keys()) != sorted(objects[i - 1].keys())):
      return False
  return True

def isValidConfig(config, defaultConfig):
  return haveSameKeys([config, defaultConfig])

def read_config(defaultConfig, configPath = "./config.json", throwErrs = False):
  try:
    configFile = open(configPath, "r")
    config = json.loads(configFile.read())

    if not isValidConfig(config, defaultConfig):
      if (throwErrs):
        raise SystemExit(f"Fatal Error: {configPath} invalid project config")
      print(f"Error: {configPath} invalid project config. Using default config...")
      return defaultConfig
    return config

  except (PermissionError, json.JSONDecodeError) as e:
    if (throwErrs):
      raise SystemExit(e)
    print(f"Encountered {e} trying to read {configPath}. Using default config...")
    return defaultConfig

  except FileNotFoundError as e:
    print(f"FileNotFoundError: Failed to locate {configPath}")
    print("Creating with default settings...")
    f = open(configPath, "a")
    f.write(json.dumps(defaultConfig))
    f.close()
    return defaultConfig

def readCache(cachePath = "./cache.json", throwErrs = False):
  try:
    cacheFile = open(cachePath, "r")
    cache = json.loads(cacheFile.read())
    return cache

  except (PermissionError, json.JSONDecodeError) as e:
    if (throwErrs):
      raise SystemExit(e)
    print(f"Encountered {e} trying to read {cachePath}")
    return {}

  except FileNotFoundError as e:
    print(f"FileNotFoundError: Failed to locate {cachePath}")
    f = open(cachePath, "a")
    f.write(json.dumps({}))
    f.close()
    return {}