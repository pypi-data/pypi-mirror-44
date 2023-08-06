from pathlib import Path
import fire

def generate(*args, **kwargs):
    import RemoveMedia.configuration.generate_config as gc
    name, path = gc.generate_config(*args, **kwargs)
    print(f"{name} is created at {path}")
    
def remove(*args, **kwargs):
    from RemoveMedia.manipulation.remove import Remove
    rm = Remove(*args, **kwargs)
    rm.delete()

if __name__ == "__main__": #pragma: no cover
    fire.Fire()